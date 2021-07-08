import cv2
import time
import HandTrackingModule as htm
from resize import formattingImage, crop, transform
from transform import four_point_transform

cap = cv2.VideoCapture('https://192.168.137.229:8080/video')


overlayList = []

print(len(overlayList))
pTime = 0

detector = htm.handDetector()
cropCheck = True
tipIds = [4, 8, 12, 16, 20]


point = []

cropOn = False

while True:
    siuccess, img = cap.read()
    try:
        if cropCheck:
            point = crop(img)
            warped = four_point_transform(img, point)
            img = cv2.resize(warped, (int(750), int(750)),
                            interpolation=cv2.INTER_CUBIC)
            cropCheck = False

        warped = four_point_transform(img, point)
        img = cv2.resize(warped, (int(750), int(750)),
                        interpolation=cv2.INTER_CUBIC)

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)




        if len(lmList) != 0:
            id = 9
            img = cv2.circle(img, (lmList[9][1], lmList[9][2]), radius=5, color=(100, 40, 40), thickness=-1)
            print(round(lmList[9][1] * 1.33333333), round(lmList[9][2] * 1.33333333))

            cv2.putText(img, f'x: {int(round(lmList[9][1] * 1.33333333))}mm, y: {round(lmList[9][2] * 1.33333333)}mm', (10, 130), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)


            fingers = []

            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)


            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            print(fingers)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime


        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)




        cv2.imshow("Image", img)
        cv2.waitKey(1)
    except:
        pass
