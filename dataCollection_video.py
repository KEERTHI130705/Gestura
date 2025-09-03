import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time


cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)


offset = 20
imgSize = 300


# Video writers (None until 'r' pressed)
out_main = None
out_crop = None
recording = False


while True:
    success, img = cap.read()
    if not success:
        break


    hands, img = detector.findHands(img)  # detect hands
    imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
    imgCrop = None


    if hands and len(hands) == 2:  # only record when two hands detected
        x_min = min(hands[0]['bbox'][0], hands[1]['bbox'][0])
        y_min = min(hands[0]['bbox'][1], hands[1]['bbox'][1])
        x_max = max(hands[0]['bbox'][0] + hands[0]['bbox'][2],
                    hands[1]['bbox'][0] + hands[1]['bbox'][2])
        y_max = max(hands[0]['bbox'][1] + hands[0]['bbox'][3],
                    hands[1]['bbox'][1] + hands[1]['bbox'][3])


        # crop both hands together
        imgCrop = img[y_min - offset:y_max + offset, x_min - offset:x_max + offset]


        if imgCrop.size != 0:
            h, w, _ = imgCrop.shape
            aspectRatio = h / w


            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize


            cv2.imshow("Cropped Hands", imgWhite)


            if recording:
                out_main.write(img)
                out_crop.write(imgWhite)


    cv2.imshow("Main Video", img)


    key = cv2.waitKey(1)


    # Start/stop recording
    if key == ord('r'):
        if not recording:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out_main = cv2.VideoWriter(f'output_full_{time.time()}.avi', fourcc, 20.0,
                                       (img.shape[1], img.shape[0]))
            out_crop = cv2.VideoWriter(f'output_crop_{time.time()}.avi', fourcc, 20.0,
                                       (imgSize, imgSize))
            print("Recording started...")
            recording = True
        else:
            print("Recording stopped.")
            recording = False
            out_main.release()
            out_crop.release()


    elif key == ord('q'):
        break


cap.release()
if out_main: out_main.release()
if out_crop: out_crop.release()
cv2.destroyAllWindows()
