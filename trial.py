import cv2
import time
import io
import numpy as np
import pandas as pd
import pygame
import warnings
from gtts import gTTS
from spellchecker import SpellChecker
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

import streamlit_demo.hand_detector2 as hdm  # your custom detector

warnings.filterwarnings("ignore")

# -----------------------------
# Load dataset + train model
# -----------------------------
data = pd.read_csv("hand_signals.csv")
data = data.loc[:, ~data.columns.str.contains("^Unnamed")]

X = data.drop("letter", axis=1)
y = data["letter"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

spell = SpellChecker()


# -----------------------------
# Speech function
# -----------------------------
def speech(text):
    myobj = gTTS(text=text, lang="en", slow=False)
    mp3_fp = io.BytesIO()
    myobj.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    pygame.mixer.music.load(mp3_fp, "mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# -----------------------------
# Main Kivy App
# -----------------------------
class HandSignApp(App):
    def build(self):
        pygame.mixer.init()

        self.detector = hdm.handDetector()
        self.cap = cv2.VideoCapture(0)

        # --- Widgets ---
        self.img_widget = Image(size_hint=(1, 0.75))  # webcam 75% height
        self.pred_label = Label(
            text="Live Guess: ",
            font_size="24sp",
            size_hint=(1, 0.08),
            color=(1, 1, 0, 1),
        )
        self.word_label = Label(
            text="Current Word: ",
            font_size="22sp",
            size_hint=(1, 0.07),
            color=(0, 1, 0, 1),
        )
        self.words_label = Label(
            text="Completed Words: ",
            font_size="20sp",
            size_hint=(1, 0.07),
            color=(0, 1, 1, 1),
        )
        self.sentence_label = Label(
            text="Final Sentence: ",
            font_size="18sp",
            size_hint=(1, 0.06),
            color=(1, 0, 1, 1),
        )

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.img_widget)
        layout.add_widget(self.pred_label)
        layout.add_widget(self.word_label)
        layout.add_widget(self.words_label)
        layout.add_widget(self.sentence_label)

        # Recognition state
        self.word = ""
        self.words = []
        self.sentence = []
        self.start = time.time()
        self.end = time.time()

        self.stable_letter = None
        self.stable_count = 0
        self.stable_threshold = 15
        self.confidence_threshold = 0.7

        # Run update loop
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return layout

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)  # mirror like a webcam

        # --- Detection uses BGR (original frame) ---
        img = self.detector.find_hands(frame, draw=True)
        landmarks = self.detector.find_position(img)

        if not landmarks:
            self.handle_idle()
        elif len(landmarks) == 1:
            self.process_hand(landmarks, img)

        # --- Convert for display in Kivy (RGB) ---
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        buf = frame_rgb.tobytes()
        texture = Texture.create(
            size=(frame_rgb.shape[1], frame_rgb.shape[0]), colorfmt="rgb"
        )
        texture.blit_buffer(buf, colorfmt="rgb", bufferfmt="ubyte")
        texture.flip_vertical()
        self.img_widget.texture = texture

    def handle_idle(self):
        self.start = time.time()
        idle_timer = self.start - self.end

        # End of word (pause >= 3 sec)
        if idle_timer >= 3 and self.word != "":
            raw_word = self.word.strip()

            # Only run spellchecker if word has >1 letter
            if len(raw_word) > 1:
                corrected = spell.correction(raw_word) or raw_word
            else:
                corrected = raw_word

            print(f"Raw: {raw_word} | Corrected: {corrected}")
            speech(corrected)

            self.words.append(corrected)
            self.sentence.append(corrected)
            self.word = ""  # reset
            self.word_label.text = f"Current Word: "
            self.words_label.text = f"Completed Words: {' '.join(self.words)}"

        # End of sentence (pause >= 6 sec)
        if idle_timer >= 6 and self.sentence:
            final_sentence = " ".join(self.sentence)
            print("\nFinal Recognized Sentence:", final_sentence)
            speech(final_sentence)
            self.sentence = []  # reset
            self.sentence_label.text = f"Final Sentence: {final_sentence}"

        self.stable_letter = None
        self.stable_count = 0

    def process_hand(self, landmarks, img):
        self.end = time.time()
        lmlist = landmarks[0][1]

        location_vector = np.array(
            [coord for lm in lmlist for coord in lm[1:3]]
        ).reshape(1, -1)

        probabilities = model.predict_proba(location_vector)
        max_prob = np.max(probabilities)
        if max_prob > self.confidence_threshold:
            live_guess = model.predict(location_vector)[0]
            self.pred_label.text = f"Live Guess: {live_guess} (Stable: {self.stable_letter or '-'})"

            if self.stable_letter == live_guess:
                self.stable_count += 1
            else:
                self.stable_letter = live_guess
                self.stable_count = 1

            if self.stable_count == self.stable_threshold:
                if not self.word or self.word[-1] != live_guess:
                    self.word += live_guess
                    print("Building:", self.word)
                    self.word_label.text = f"Current Word: {self.word}"
                self.stable_count = 0

            # --- Draw bounding box around hand ---
            x_coords = [lm[1] for lm in lmlist]
            y_coords = [lm[2] for lm in lmlist]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            cv2.rectangle(img, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20), (0, 255, 0), 2)


if __name__ == "__main__":
    HandSignApp().run()