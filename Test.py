import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
from resize import formattingImage

pTime = 0
cTime = 0
#img = cv2.imread('F:/finalNTI2/image/test/IMG_20210701_134550', 0)
#cv2.VideoCapture('rtsp://192.168.1.64/1')  cap = cv2.VideoCapture('https://100.91.16.252:8080/video')
cap = cv2.VideoCapture('https://192.168.137.33:8080/video')
detector = htm.handDetector()
while True:
    success, img = cap.read()
    try:
        img = formattingImage(img)
        img = detector.findHands(img, draw=True)
        lmList = detector.findPosition(img, draw=False)
        #print(lmList)
        if len(lmList) != 0:
            id = 9
            img = cv2.circle(img, (lmList[9][1], lmList[9][2]), radius=5, color=(100, 40, 40), thickness=-1)
            print(lmList[9][1]*2, lmList[9][2]*2)
            #print(lmList[4])



        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    except:
        print('ERROR')