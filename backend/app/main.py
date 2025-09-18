import asyncio
import os
import io
import time
from typing import Optional

import cv2
import numpy as np
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import EventSourceResponse

import pandas as pd
from sklearn.linear_model import LogisticRegression

# Local imports from existing project
import sys
sys.path.append('/workspace')
import streamlit_demo.hand_detector2 as hdm

try:
    import pyvirtualcam
    _VCAM_AVAILABLE = True
except Exception:
    _VCAM_AVAILABLE = False

try:
    from gtts import gTTS
    import pygame
    _TTS_AVAILABLE = True
except Exception:
    _TTS_AVAILABLE = False


class Mode:
    LETTERS = 'letters'
    WORDS = 'words'
    SENTENCES = 'sentences'


class Recognizer:
    def __init__(self) -> None:
        self.detector = hdm.handDetector()
        self.cap = cv2.VideoCapture(0)
        self.mode = Mode.SENTENCES
        self._load_model()
        self.word = ''
        self.words = []
        self.sentence = []
        self.stable_letter: Optional[str] = None
        self.stable_count = 0
        self.stable_threshold = 15
        self.confidence_threshold = 0.7
        self.last_seen_ts = time.time()
        self.vcam_enabled = False
        self.vcam: Optional[pyvirtualcam.Camera] = None if _VCAM_AVAILABLE else None
        self.tts_enabled = False
        if _TTS_AVAILABLE:
            try:
                pygame.mixer.init()
            except Exception:
                pass

    def _load_model(self) -> None:
        data = pd.read_csv('/workspace/hand_signals.csv')
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
        X = data.drop('letter', axis=1)
        y = data['letter']
        model = LogisticRegression(max_iter=200)
        model.fit(X, y)
        self.model = model

    def read_frame(self) -> Optional[np.ndarray]:
        success, frame = self.cap.read()
        if not success:
            return None
        return cv2.flip(frame, 1)

    def predict(self, frame: np.ndarray) -> tuple[Optional[str], np.ndarray]:
        img = self.detector.find_hands(frame, draw=False)
        landmarks = self.detector.find_position(img, draw=False)
        predicted_letter: Optional[str] = None
        if landmarks and len(landmarks) == 1:
            lmlist = landmarks[0][1]
            p1 = (min(lmlist[x][1] for x in range(len(lmlist))) - 25,
                  min(lmlist[x][2] for x in range(len(lmlist))) - 25)
            p2 = (max(lmlist[x][1] for x in range(len(lmlist))) + 25,
                  max(lmlist[x][2] for x in range(len(lmlist))) + 25)
            cv2.rectangle(img, p1, p2, (255, 255, 255), 3)
            location_vector = np.array([coord for lm in lmlist for coord in lm[1:3]]).reshape(1, -1)
            probabilities = self.model.predict_proba(location_vector)
            max_prob = float(np.max(probabilities))
            if max_prob > self.confidence_threshold:
                predicted_letter = str(self.model.predict(location_vector)[0])
                cv2.putText(img, predicted_letter, (p1[0], p1[1] - 10), cv2.QT_FONT_NORMAL, 3, (255, 255, 255), 3)
                self._update_state(predicted_letter)
            else:
                self._reset_stability()
        else:
            self._handle_idle()
        return predicted_letter, img

    def _reset_stability(self) -> None:
        self.stable_letter = None
        self.stable_count = 0

    def _update_state(self, predicted_letter: str) -> None:
        if self.stable_letter == predicted_letter:
            self.stable_count += 1
        else:
            self.stable_letter = predicted_letter
            self.stable_count = 1
        if self.stable_count == self.stable_threshold:
            if not self.word or self.word[-1] != self.stable_letter:
                self.word += self.stable_letter
            self.stable_count = 0
        self.last_seen_ts = time.time()

    def _handle_idle(self) -> None:
        now = time.time()
        idle = now - self.last_seen_ts
        # word boundary after 3s idle
        if idle >= 3 and self.word != '':
            if self.mode in (Mode.WORDS, Mode.SENTENCES):
                self.words.append(self.word)
                self.sentence.append(self.word)
                if self.tts_enabled:
                    self._speak(self.word)
            self.word = ''
        # sentence boundary after 6s idle
        if idle >= 6 and self.sentence:
            final_sentence = ' '.join(self.sentence)
            if self.tts_enabled and final_sentence:
                self._speak(final_sentence)
            self.sentence = []

    def get_output_text(self) -> str:
        if self.mode == Mode.LETTERS:
            return self.word[-1] if self.word else ''
        if self.mode == Mode.WORDS:
            return ' '.join(self.words[-3:] + ([self.word] if self.word else []))
        return ' '.join(self.sentence + ([self.word] if self.word else []))

    def ensure_vcam(self, frame_shape: tuple[int, int, int]) -> None:
        if not _VCAM_AVAILABLE:
            return
        if not self.vcam and self.vcam_enabled:
            height, width = frame_shape[0], frame_shape[1]
            self.vcam = pyvirtualcam.Camera(width=width, height=height, fps=30, print_fps=False)

    def send_to_vcam(self, frame: np.ndarray) -> None:
        if not _VCAM_AVAILABLE or not self.vcam_enabled:
            return
        self.ensure_vcam(frame.shape)
        if self.vcam is None:
            return
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            self.vcam.send(rgb)
            self.vcam.sleep_until_next_frame()
        except Exception:
            pass

    def _speak(self, text: str) -> None:
        if not _TTS_AVAILABLE:
            return
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            pygame.mixer.music.load(mp3_fp, 'mp3')
            pygame.mixer.music.play()
        except Exception:
            pass


recognizer = Recognizer()

app = FastAPI(title='Gestura Backend')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/mode')
def get_mode():
    return {'mode': recognizer.mode}


@app.post('/mode/{mode}')
def set_mode(mode: str):
    mode = mode.lower()
    if mode not in (Mode.LETTERS, Mode.WORDS, Mode.SENTENCES):
        return {'ok': False, 'error': 'invalid mode'}
    recognizer.mode = mode
    return {'ok': True, 'mode': recognizer.mode}


async def mjpeg_generator():
    boundary = 'frame'
    while True:
        frame = recognizer.read_frame()
        if frame is None:
            await asyncio.sleep(0.01)
            continue
        _, img = recognizer.predict(frame)
        text = recognizer.get_output_text()
        if text:
            cv2.putText(img, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        # mirror subtitle onto outgoing virtual cam if enabled
        recognizer.send_to_vcam(img)
        ret, jpeg = cv2.imencode('.jpg', img)
        if not ret:
            await asyncio.sleep(0.01)
            continue
        chunk = (b"--" + boundary.encode() + b"\r\n"
                 b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n")
        yield chunk
        await asyncio.sleep(0.03)


@app.get('/stream')
def stream():
    return StreamingResponse(mjpeg_generator(), media_type='multipart/x-mixed-replace; boundary=frame')


async def events_generator():
    last_text = ''
    while True:
        text = recognizer.get_output_text()
        if text != last_text:
            yield {'event': 'text', 'data': text}
            last_text = text
        await asyncio.sleep(0.1)


@app.get('/events')
async def events():
    return EventSourceResponse(events_generator())


@app.post('/vcam/{enabled}')
def toggle_vcam(enabled: bool):
    recognizer.vcam_enabled = enabled and _VCAM_AVAILABLE
    if not recognizer.vcam_enabled and recognizer.vcam:
        try:
            recognizer.vcam.close()
        except Exception:
            pass
        recognizer.vcam = None
    return {'ok': True, 'vcam': recognizer.vcam_enabled, 'available': _VCAM_AVAILABLE}


@app.post('/tts/{enabled}')
def toggle_tts(enabled: bool):
    recognizer.tts_enabled = enabled and _TTS_AVAILABLE
    return {'ok': True, 'tts': recognizer.tts_enabled, 'available': _TTS_AVAILABLE}


@app.post('/speak')
def speak(text: str):
    recognizer._speak(text)
    return {'ok': True}

