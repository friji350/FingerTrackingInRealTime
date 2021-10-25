from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QLabel, QVBoxLayout, QListWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import sys
import cv2
import time
import math
import serial
import HandTrackingModule as htm
from resize import formattingImage, crop, transform
from transform import four_point_transform
from numpy import *
import krest_trest
import telnetlib


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)

        overlayList = []

        pTime = 0

        detector = htm.handDetector()
        cropCheck = True
        tipIds = [4, 8, 12, 16, 20]
        point = []
        flag_rotate = True
        rotate_num = 90

        while True:
            siuccess, img = cap.read()
            try:
                point = crop(img)
                warped = four_point_transform(img, point)
                img = cv2.resize(warped, (int(600), int(700)),
                                 interpolation=cv2.INTER_CUBIC)
                img = detector.findHands(img)
                lmList = detector.findPosition(img, draw=False)
                if len(lmList) != 0:
                    id = 9
                    img = cv2.circle(img, (lmList[9][1], lmList[9][2]), radius=5, color=(100, 40, 40), thickness=-1)
                    img = cv2.circle(img, (lmList[0][1], lmList[0][2]), radius=5, color=(100, 40, 40), thickness=-1)
                    x = int(lmList[9][1]) * 2.5
                    y = int(lmList[9][2]) * 2.5
                    rxox = 300
                    rxoy = 0
                    trox = x
                    troy = y
                    try:
                        angle = math.atan((rxoy - troy) / (rxox - trox))
                    except:
                        angle = 90
                    x1 = rxox
                    x2 = trox
                    if x1 > x2:
                        angle += math.pi
                    angle = round(math.degrees(angle))
                    x_robot = -round(((math.fabs(math.sqrt((x - 600) ** 2 + (y - 0) ** 2))) / 40), 2)
                    x_robot += 0.02
                    f = 1233
                    w = 0.07
                    dis = math.sqrt(((lmList[9][1] - lmList[0][1]) * (lmList[9][1] - lmList[0][1])) + (
                                (lmList[9][2] - lmList[0][2]) * (lmList[9][2] - lmList[0][2])))
                    print(dis)
                    y_robot = 90 - ((7 * f) / dis)
                    if y_robot >= -20 and y_robot <= 8:
                        if rotate_num > 145:
                            y_robot = 0
                        else:
                            y_robot = 4
                    elif y_robot >= 8 and y_robot <= 25:
                        y_robot = 12.5
                    elif y_robot >= 25 and y_robot <= 30:
                        y_robot = 27.5
                    else:
                        y_robot = 12.5
                    fingers = []
                    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    for id in range(1, 5):
                        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    cv2.putText(img, str(x_robot), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                                3, (255, 0, 0), 3)
                    cv2.putText(img, str(y_robot), (10, 170), cv2.FONT_HERSHEY_PLAIN,
                                3, (255, 0, 0), 3)
                    if angle < 180:
                        krest_trest.go_to([x_robot, y_robot], angle, flag_rotate)
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.imshow("Image", img)
                cv2.waitKey(1)
                self.change_pixmap_signal.emit(img)
            except:
                pass

        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        self.image_label.move(120, 160)
        self.textLabel = QLabel('Webcam')
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        self.setLayout(vbox)
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)

        self.pybutton = QPushButton('go_to 20, 20, 20', self)
        self.pybutton.resize(100, 32)
        self.pybutton.move(650, 50)
        # self.closeButton.clicked.connect(self.go_to_20)

        self.setGeometry(250, 250, 1280, 720)
        self.thread.start()
        self.show()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())



