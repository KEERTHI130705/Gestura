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

# Ignore all warnings
warnings.filterwarnings("ignore")

# Read and process data
data = pd.read_csv('hand_signals.csv')
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

X = data.drop('letter', axis=1)
y = data['letter']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

spell = SpellChecker()  # autocorrect engine

def speech(text):
    """
    Converts a piece of text into speech using pyGame and gTTS libraries
    """
    myobj = gTTS(text=text, lang='en', slow=False)
    mp3_fp = io.BytesIO()
    myobj.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def main():
    pygame.mixer.init()
    signal_data = {}
    cap = cv2.VideoCapture(0)
    detector = hdm.handDetector()
    letters = []
    word = ''
    words = []
    sentence = []  # Add this at the start of main()
    start = time.time()
    end = time.time()

    stable_letter = None
    stable_count = 0
    stable_threshold = 15  # Number of consecutive frames for stability

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        key = cv2.waitKey(1) & 0xFF

        img = detector.find_hands(img, draw=False)
        landmarks = detector.find_position(img)

        confidence_threshold = .7

        # No hands → check idle time
        if not landmarks:
            start = time.time()
            idle_timer = start - end

            # End of word
            if idle_timer >= 3 and word != '':
                if word[-1] != ' ':
                    corrected = spell.correction(word.strip())
                    if corrected is None:
                        corrected = word.strip()
                    print(f"Raw: {word}  |  Corrected: {corrected}")
                    speech(corrected)
                    words.append(corrected)
                    sentence.append(corrected)  # Add word to sentence
                    word = ''

            # End of sentence (longer pause)
            if idle_timer >= 6 and sentence:
                final_sentence = " ".join(sentence)
                print("\nFinal Recognized Sentence:", final_sentence)
                speech(final_sentence)
                sentence = []  # Reset for next sentence

            # Reset stability when no hand
            stable_letter = None
            stable_count = 0

        if landmarks and len(landmarks) == 1:
            lmlist = landmarks[0][1]
            end = time.time()

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

                # Stability logic
                if stable_letter == predicted_letter:
                    stable_count += 1
                else:
                    stable_letter = predicted_letter
                    stable_count = 1

                # Only append if stable for threshold frames
                if stable_count == stable_threshold:
                    if not word or word[-1] != stable_letter:
                        word += stable_letter
                        print("Building:", word)
                    stable_count = 0  # Reset after appending

                cv2.putText(img, predicted_letter, (p1[0], p1[1] - 10),
                            cv2.QT_FONT_NORMAL, 3, (255, 255, 255), 3)

        # Show the frame with predictions
        cv2.imshow("Image", img)

        # Collect signals if 'c' pressed
        if key == ord('c') and landmarks:
            for item in lmlist:
                if f'{item[0]}x' in signal_data:
                    signal_data[f'{item[0]}x'].append(item[1])
                else:
                    signal_data[f'{item[0]}x'] = [item[1]]
                if f'{item[0]}y' in signal_data:
                    signal_data[f'{item[0]}y'].append(item[2])
                else:
                    signal_data[f'{item[0]}y'] = [item[2]]

        if key == ord('q'):
            break

    # Save extra signals if collected
    if signal_data:
        signal_data['letter'] = ['a'] * len(signal_data['0x'])
        new_signals = pd.DataFrame(signal_data)
        existing_signals = pd.read_csv('hand_signals.csv')
        updated_stats = pd.concat([existing_signals, new_signals], ignore_index=True)
        updated_stats.to_csv('hand_signals.csv', index=False)

    # Final sentence after quitting
    if words:
        final_sentence = " ".join(words)
        print("\n✨ Final Recognized Sentence:", final_sentence)
        speech(final_sentence)

if __name__ == '__main__':
    main()
