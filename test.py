
import cv2
import numpy as np
import tensorflow as tf
from cvzone.HandTrackingModule import HandDetector


# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="Model/model_unquant.tflite")
interpreter.allocate_tensors()


input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)


imgSize = 300
offset = 20


# Labels
labels = ["A", "B", "C","D", "E", "F", "G", "I", "K", "L", "M", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y","Z","H","N"]


while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)


    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']


        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]


        try:
            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = int(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = (imgSize - wCal) // 2
                imgWhite[:, wGap:wGap + wCal] = imgResize
            else:
                k = imgSize / w
                hCal = int(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = (imgSize - hCal) // 2
                imgWhite[hGap:hGap + hCal, :] = imgResize


            # Preprocess for model
            imgInput = cv2.resize(imgWhite, (224, 224))   # Teachable Machine usually exports 224x224
            imgInput = np.expand_dims(imgInput, axis=0).astype(np.float32) / 255.0


            # Run inference
            interpreter.set_tensor(input_details[0]['index'], imgInput)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            index = np.argmax(output_data)
            prediction = output_data[0]


            # Show label
            cv2.putText(imgOutput, labels[index], (x, y - 26),
                        cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 0, 255), 2)


            print("Prediction:", prediction, "Class:", labels[index])


        except Exception as e:
            print("Error:", e)


    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)
