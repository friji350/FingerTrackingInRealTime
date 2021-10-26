from os import name
from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QLabel, QVBoxLayout, QListWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import sys
import cv2
import time
import math
import sqlite3
import HandTrackingModule as htm
from resize import formattingImage, crop, transform
from transform import four_point_transform
from numpy import *
import krest_trest
import telnetlib
import  datetime

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self._record_start =False
        self.new_script = str()

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
        self.noArm = 0
        self.parkFlag = True
        while True:
            siuccess, img = cap.read()
            if self._run_flag:
                try:
                    point = crop(img)
                    warped = four_point_transform(img, point)
                    img = cv2.resize(warped, (int(600), int(700)),
                                     interpolation=cv2.INTER_CUBIC)
                    img = detector.findHands(img)
                    lmList = detector.findPosition(img, draw=False)
                    if len(lmList) != 0:
                        self.parkFlag = True
                        self.noArm = 0
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
                                y_robot = 8
                        elif y_robot >= 8 and y_robot <= 25:
                            y_robot = 17.5
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
                            angle_ik = krest_trest.go_to([x_robot, y_robot], angle, flag_rotate)
                            if self._record_start:
                                self.new_script += f"{angle_ik} \n"
                    else:
                        if self.noArm >= 40 and self.parkFlag:
                            print(123)
                            self.parkFlag = False
                            str_send = f"B60"
                            telnet = telnetlib.Telnet('192.168.1.159')
                            telnet.write(str_send.encode())
                            time.sleep(2)
                            str_send = 'C90'
                            telnet.write(str_send.encode())
                            time.sleep(2)
                            str_send = 'A90'
                            telnet.write(str_send.encode())
                            time.sleep(2)

                            str_send = 'D150 B55 C8'
                            telnet.write(str_send.encode())
                            time.sleep(2)
                        else:
                            self.noArm += 1


                    cTime = time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime
                    self.change_pixmap_signal.emit(img)
                except:
                    pass
            else:
                pass
        cap.release()

    def stop(self):
        self._run_flag = False

    def start_(self):
        self._run_flag = True

    def parkFlafFalse(self):
        self.parkFlag = True
    
    def recordStart(self):
        self._record_start = True

    
    def recordEnd(self, tool):
        self._record_start = False
        self.name = str(random.randint(1, 1000000))
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"insert into Scripts values (Null, '{self.name}', '{tool}ᅠ{self.new_script}')")
        conn.commit()
        conn.close()
        self.new_script = ''
        return name




class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        uic.loadUi("G:/FingerTrackingInRealTime-main/main.ui", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        self.image_label.move(20, 20)
        self.image_label.setStyleSheet("background-color: #C4C4C4")
        self.textLabel = QLabel('Webcam')
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.scriptLoad()
        self.pushButton.clicked.connect(self.scriptStart)
        self.pushButton_2.clicked.connect(self.recordStart)
        self.pushButton_3.clicked.connect(self.recordEnd)
        self.pushButton_4.clicked.connect(self.goTo)
        self.pushButton_5.clicked.connect(self.toolBolt)
        self.pushButton_6.clicked.connect(self.toolZahvet)
        self.thread.start()
        self.pushButton_3.hide()
        self.horizontalSlider.valueChanged.connect(self.horizontalSlider_changed)
        self.show()
        self.tool = None
        self.tool_new = None

    def toolBolt(self):
        self.tool_new = 'Болт'
        if self.tool_new != self.tool:
            print(321)
            self.toolChanger()
        else:
            self.tool_new = None

    def toolZahvet(self):
        print(321)
        self.tool_new = 'Захват'
        if self.tool_new != self.tool:
            self.toolChanger()
        else:
            self.tool_new = None

    def toolChanger(self):
        if self.tool is not None:
            if self.tool == 'Захват':
                print('отдал завхат')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 3")
                results = cursor.fetchall()
                print(results[0][0])
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    print(str_send)
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.thread.start_()
            elif self.tool == 'Болт':
                print('отдал болт')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 5")
                results = cursor.fetchall()
                print(results[0][0])
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    print(str_send)
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.thread.start_()

            if self.tool_new == 'Захват':
                print('взял захват')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 1")
                results = cursor.fetchall()
                print(results[0][0])
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.tool = self.tool_new
                self.tool_new = None
                self.thread.start_()
            elif self.tool_new == 'Болт':
                print('взял Болт')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 4")
                results = cursor.fetchall()
                print(results[0][0])
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.tool = self.tool_new
                self.tool_new = None
                self.thread.start_()
        else:
            print(self.tool_new)
            if self.tool_new == 'Захват':
                print('взял захват')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 1")
                results = cursor.fetchall()
                print(results[0][0])
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.thread.start_()
                self.tool = self.tool_new
                self.tool_new = None
            elif self.tool_new == 'Болт':
                print('взял Болт')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 4")
                results = cursor.fetchall()
                print(results[0][0])
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.tool = self.tool_new
                self.tool_new = None
                self.thread.start_()
        self.thread.parkFlafFalse()


    def goTo(self):
        x_robot = float(self.lineEdit.text()) * -1
        y_robot = float(self.lineEdit_2.text())
        angle_ik = krest_trest.go_to([x_robot, y_robot], 90, True)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.thread.parkFlafFalse()

    def horizontalSlider_changed(self):
        self.label.setText(str(self.horizontalSlider.value()))
        str_new = f'A{self.horizontalSlider.value()}'
        telnet = telnetlib.Telnet('192.168.1.159')
        telnet.write(str_new.encode())
        time.sleep(0.2)

    def scriptLoad(self):
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Scripts")
        results = cursor.fetchall()
        id_official = [1, 2, 3, 4, 5]
        for i in results:
            if not int(i[0]) in id_official:
                self.listWidget.addItem(f"{str(i[0])}ᅠ{str(i[1])}")
        conn.close()
    
    def recordStart(self):
        self.thread.recordStart()
        self.pushButton_3.show()

    def scriptStart(self):
        self.thread.stop()
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        item = self.listWidget.currentItem()
        if item is not None:
            cursor.execute(f"SELECT script FROM Scripts WHERE id = {item.text().split('ᅠ')[0]}")
            results = cursor.fetchall()
            tool_new1 = results[0][0].split("ᅠ")[0]
            scrii = results[0][0].split("ᅠ")[1]
            if tool_new1 == 'Захват' and self.tool != 'Захват':
                print('Взял захват')
                self.toolZahvet()
            elif tool_new1 == 'Болт' and self.tool != 'Болт':
                print('Взял болт')
                self.toolBolt()
            for i in scrii.split('\n'):
                str_send = f"{i}"
                telnet = telnetlib.Telnet('192.168.1.159')
                telnet.write(str_send.encode())
                time.sleep(0.1)
            conn.close()
        self.thread.start_()
        self.thread.parkFlafFalse()


    def recordEnd(self):
        self.thread.recordEnd(self.tool)
        self.pushButton_3.hide()
        self.listWidget.clear()
        self.scriptLoad()

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



