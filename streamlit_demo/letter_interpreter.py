import hand_detector2 as hdm
import cv2
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import time
from gtts import gTTS
import io
import pygame
import warnings
from spellchecker import SpellChecker  # 🔥 autocorrect
import streamlit as st

# Ignore warnings
warnings.filterwarnings("ignore")

# Load dataset
data = pd.read_csv('hand_signals.csv')
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

X = data.drop('letter', axis=1)
y = data['letter']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

spell = SpellChecker()  # autocorrect engine

def speech(text):
    """Convert text to speech and return mp3 binary for Streamlit to play"""
    myobj = gTTS(text=text, lang='en', slow=False)
    mp3_fp = io.BytesIO()
    myobj.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

def main():
    st.title("✋ Hand Gesture to Speech Recognition")
    st.markdown("Real-time **hand signal recognition → autocorrect → speech output**")

    run_app = st.checkbox("▶ Start Camera", value=False)

    if run_app:
        stframe = st.empty()
        cap = cv2.VideoCapture(0)
        detector = hdm.handDetector()

        signal_data = {}
        word = ''
        words = []
        sentence = []

        start = time.time()
        end = time.time()

        stable_letter = None
        stable_count = 0
        stable_threshold = 15
        confidence_threshold = 0.7

        while run_app:
            success, img = cap.read()
            if not success:
                st.warning("⚠ Camera not detected.")
                break

            img = cv2.flip(img, 1)
            img = detector.find_hands(img, draw=False)
            landmarks = detector.find_position(img)

            # idle check
            if not landmarks:
                start = time.time()
                idle_timer = start - end

                if idle_timer >= 3 and word != '':
                    if word[-1] != ' ':
                        corrected = spell.correction(word.strip())
                        if corrected is None:
                            corrected = word.strip()
                        st.write(f"Raw: {word} | Corrected: {corrected}")
                        words.append(corrected)
                        sentence.append(corrected)
                        word = ''

                if idle_timer >= 6 and sentence:
                    final_sentence = " ".join(sentence)
                    st.success(f"✨ Final Recognized Sentence: {final_sentence}")
                    st.audio(speech(final_sentence), format="audio/mp3")
                    sentence = []

                stable_letter = None
                stable_count = 0

            # hand detected
            if landmarks and len(landmarks) == 1:
                end = time.time()
                lmlist = landmarks[0][1]

                p1 = (min(lmlist[x][1] for x in range(len(lmlist))) - 25,
                      min(lmlist[x][2] for x in range(len(lmlist))) - 25)
                p2 = (max(lmlist[x][1] for x in range(len(lmlist))) + 25,
                      max(lmlist[x][2] for x in range(len(lmlist))) + 25)
                cv2.rectangle(img, p1, p2, (255, 255, 255), 3)

                location_vector = np.array([coord for lm in lmlist for coord in lm[1:3]]).reshape(1, -1)

                probabilities = model.predict_proba(location_vector)
                max_prob = np.max(probabilities)
                if max_prob > confidence_threshold:
                    predicted_letter = model.predict(location_vector)[0]

                    if stable_letter == predicted_letter:
                        stable_count += 1
                    else:
                        stable_letter = predicted_letter
                        stable_count = 1

                    if stable_count == stable_threshold:
                        if not word or word[-1] != stable_letter:
                            word += stable_letter
                            st.write(f"Building Word: {word}")
                        stable_count = 0

                    cv2.putText(img, predicted_letter, (p1[0], p1[1] - 10),
                                cv2.QT_FONT_NORMAL, 3, (255, 255, 255), 3)

            # display live frame
            stframe.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), channels="RGB")

        cap.release()

        if words:
            final_sentence = " ".join(words)
            st.success(f"✨ Final Recognized Sentence: {final_sentence}")
            st.audio(speech(final_sentence), format="audio/mp3")

if __name__ == "__main__":
    main()

# To run the app, use the command:
# streamlit run letter_interpreter.py    

#pip list