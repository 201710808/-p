import cv2
import numpy as np
import sys
import random

from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QFont, QMovie
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import webbrowser

global x
x = 0
global lower_x
lower_x = 0
global upper_x
upper_x = 0
global file_name
global flag
flag = 0


class Thread1(QThread):
    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        global file_name
        tongue_detection(file_name)
        global flag
        flag = 1
        # print("\nfinished")


class TitlePage(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tongue')
        # self.move(700, 0)
        # self.resize(467, 960)

        self.button = QPushButton('', self)
        self.button.setGeometry(QRect(0, 0, 467, 960))
        self.button.setStyleSheet("QPushButton{background-image: url(resource/title.png)}")
        self.button.clicked.connect(self.changePage)

    def changePage(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AnalyzePage(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # def display_img(self):
    #     original_img, result_img = tongue_detection()
    #     self.pixmap = QPixmap(original_img)

    def initUI(self):
        self.setWindowTitle('Tongue')
        # self.move(700, 0)
        # self.resize(467, 960)

        # b1 = QPushButton('Detect Tongue', self)
        # b1.move(25, 18)
        # b1.clicked.connect(self.dialog_open)
        #
        # self.dialog = QDialog()

        self.background = QLabel(' ', self)
        self.background.setGeometry(QRect(0, 0, 467, 960))
        self.background.setStyleSheet("QLabel{background-image: url(resource/inform.png)}")

        self.button = QPushButton('+', self)
        self.button.clicked.connect(self.filedialog_open)
        self.button.setGeometry(QRect(143, 120, 180, 180))
        font = self.button.font()
        font.setPointSize(50)
        font.setBold(True)
        self.button.setFont(font)
        # self.button.move(180, 900)

        self.example_button = QPushButton('', self)
        self.example_button.resize(54, 32)
        self.example_button.move(82, 492)
        self.example_button.setStyleSheet("QPushButton{background-image: url(resource/example.png)}")
        # font2 = self.example_button.font()
        # font2.setPointSize(20)
        # font2.setBold(True)
        # self.example_button.setFont(font2)
        self.example_button.setToolTip('<img src="resource/예시.png">')

        self.b4 = QPushButton('다음', self)
        self.b4.move(345, 895)
        self.b4.clicked.connect(self.nextPage)
        self.b4.hide()

        self.b5 = QPushButton('이전', self)
        self.b5.move(22, 895)
        self.b5.clicked.connect(self.prevPage)

        self.loading_screen = QLabel(' ', self)
        self.loading_screen.setGeometry(QRect(0, 0, 467, 960))
        self.loading_screen.setStyleSheet("QLabel{background-image: url(resource/black.png)}")
        self.loading_screen.hide()


        self.loading_img = QLabel(' ', self)
        # self.loading_img.setGeometry(QRect(201, 448, 64, 64))
        self.loading_img.setGeometry(QRect(int(467 / 2 - 68), int(960 / 2 - 95), 200, 200))
        self.movie = QMovie('resource/Hourglass.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.loading_img.setMovie(self.movie)
        self.movie.start()
        self.loading_img.hide()

        self.title = QLabel('', self)
        self.title.setStyleSheet("QLabel{background-image: url(resource/사진선택.png)}")
        self.title.setGeometry(QRect(0, 0, 467, 76))


        # self.label3 = QLabel('주의사항', self)
        # self.label3.setStyleSheet("color: #000000; border-style: solid; border-width: 2px; border-color: "
        #                           "#080808; border-radius: 10px; ")
        # self.label3.setGeometry(QRect(20, 350, 430, 450))
        # self.label3.setAlignment(Qt.AlignTop)
        # font3 = self.label3.font()
        # font3.setPointSize(12)
        # self.label3.setFont(font3)
        # test_text = 'ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ'

    def nextPage(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def prevPage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def filedialog_open(self):
        # self.loading_screen.show()
        # self.loading_img.show()
        fname = QFileDialog.getOpenFileName(self, 'Open File', '', 'Image File(*.png *.jpg)')
        global file_name
        file_name = fname[0]
        if fname[0]:
            self.loading_screen.show()
            self.loading_img.show()
            Thread1(self).start()
            # tongue_detection(fname[0])
            # while True:
            #     global flag
            #     if flag == 1:
            #         print("end")
            #         self.button.setStyleSheet("QPushButton{background-image: url(tongue_result.jpg)}")
            #         self.button.setText(' ')
            #         self.b4.show()
            #         flag = 0
            #         self.loading_screen.hide()
            #         self.loading_img.hide()
            #         break
            #     else:
            #         print("pass")
            #         continue
            self.timer = QTimer()
            self.timer.setInterval(100)
            self.timer.timeout.connect(self.refreshImage)
            self.timer.start()

        else:
            QMessageBox.about(self, 'Warning', '파일을 선택하지 않았습니다.')
            # self.loading_screen.hide()
            # self.loading_img.hide()

    def dialog_close(self):
        self.dialog.close()

    def refreshImage(self):
        global flag
        if flag == 1:
            # print("end")
            self.button.setStyleSheet("QPushButton{background-image: url(tongue_result.jpg)}")
            self.button.setText(' ')
            self.b4.show()
            flag = 0
            self.loading_screen.hide()
            self.loading_img.hide()
            self.timer.stop()
        else:
            # print("pass")
            pass


class ResultPage(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # def display_img(self):
    #     original_img, result_img = tongue_detection()
    #     self.pixmap = QPixmap(original_img)

    def refreshImage(self):
        self.label.setStyleSheet("QLabel{background-image: url(tongue_result.jpg)}")
        y = 305 - (x / 100 * 305)

        # text_good = '백태 상태: 양호'
        # text_normal = '백태 상태: 중간'
        # text_warning = '백태 상태: 심각'

        # text_good_upper = '혀 중앙부 백태 상태: 양호\n\n혓바닥이 건강한 상태입니다.'
        # text_warning_upper = '혀 중앙부 백태 상태: 주의\n\n소화 계통에 문제가 있을 가능성이 있습니다.'
        #
        # text_good_lower = '혀 하단부 백태 상태: 양호\n\n혓바닥이 건강한 상태입니다.'
        # text_warning_lower = '혀 하단부 백태 상태: 주의\n\n순환 계통에 문제가 있을 가능성이 있습니다.'

        # text_222 = 'ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ'
        # text_000 = '심각 심각'
        # text_010 = '보통 심각'
        # text_001 = '심각 보통'
        # text_011 = '보통 보통'
        # text_002 = '심각 양호'
        # text_020 = '양호 심각'
        # text_022 = '양호 양호'
        # text_012 = '보통 양호'
        # text_021 = '양호 보통'
        #
        # text_100 = '심각 심각'
        # text_110 = '보통 심각'
        # text_101 = '심각 보통'
        # text_111 = '보통 보통'
        # text_102 = '심각 양호'
        # text_120 = '양호 심각'
        # text_122 = '양호 양호'
        # text_112 = '보통 양호'
        # text_121 = '양호 보통'
        #
        # text_200 = '심각 심각'
        # text_210 = '보통 심각'
        # text_201 = '심각 보통'
        # text_211 = '보통 보통'
        # text_202 = '심각 양호'
        # text_220 = '양호 심각'
        # text_222 = '양호 양호'
        # text_212 = '보통 양호'
        # text_221 = '양호 보통'

        # 전체 심각일 때
        if x <= 42 and x != 0:
            y = 305 - (x / 42 * (305 / 3))
            # self.label1.setText(text_warning)
            # 심각 심각
            if (upper_x <= 42 and upper_x != 0) and (lower_x <= 42 and lower_x != 0):
                self.background.setStyleSheet("QLabel{background-image: url(resource/1심각심각심각.PNG)}")
                # self.label3.setText(text_000)
            # 보통 심각
            elif (42 < upper_x <= 68) and (lower_x <= 42 and lower_x != 0):
                self.background.setStyleSheet("QLabel{background-image: url(resource/4심각보통심각.PNG)}")
                # self.label3.setText(text_010)
            # 보통 보통
            elif (42 < upper_x <= 68) and (42 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/5심각보통보통.PNG)}")
                # self.label3.setText(text_011)
            # 심각 보통
            elif (upper_x <= 42 and upper_x != 0) and (42 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/2심각심각보통.PNG)}")
                # self.background.setStyleSheet("QLabel{background-image: url(2페이지_임시4.PNG)}")
                # self.label3.setText(text_001)
            # 심각 양호
            elif (upper_x <= 42 and upper_x != 0) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/3심각심각양호.PNG)}")
                # self.label3.setText(text_002)
            # 양호 심각
            elif (upper_x > 68) and (lower_x <= 68 and lower_x != 0):
                self.background.setStyleSheet("QLabel{background-image: url(resource/7심각양호심각.PNG)}")
                # self.label3.setText(text_020)
            # 양호 양호
            elif (upper_x > 68) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/9심각양호양호.PNG)}")
                # self.label3.setText(text_022)
            # 보통 양호
            elif (42 < upper_x <= 68) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/6심각보통양호.PNG)}")
                # self.label3.setText(text_012)
            # 양호 보통
            elif (upper_x > 68) and (42 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/8심각양호보통.PNG)}")
                # self.label3.setText(text_021)

        elif 68 >= x > 42:
            y = (305 / 3 * 2) - ((x - 42) / 26 * (305 / 3))
            # self.label1.setText(text_normal)
            # 심각 심각
            if (upper_x <= 42 and upper_x != 0) and (lower_x <= 42 and lower_x != 0):
                self.background.setStyleSheet("QLabel{background-image: url(resource/10보통심각심각.PNG)}")
                # self.label3.setText(text_100)
            # 보통 심각
            elif (42 < upper_x <= 68) and (lower_x <= 42 and lower_x != 0):
                self.background.setStyleSheet("QLabel{background-image: url(resource/13보통보통심각.PNG)}")
                # self.label3.setText(text_110)
            # 보통 보통
            elif (42 < upper_x <= 68) and (42 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/14보통보통보통.PNG)}")
                # self.label3.setText(text_111)
            # 심각 보통
            elif (upper_x <= 42 and upper_x != 0) and (42 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/11보통심각보통.PNG)}")
                # self.label3.setText(text_101)
            # 심각 양호
            elif (upper_x <= 42 and upper_x != 0) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/12보통심각양호.PNG)}")
                # self.label3.setText(text_102)
            # 양호 심각
            elif (upper_x > 68) and (lower_x <= 68 and lower_x != 0):
                self.background.setStyleSheet("QLabel{background-image: url(resource/16보통양호심각.PNG)}")
                # self.label3.setText(text_120)
            # 양호 양호
            elif (upper_x > 68) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/18보통양호양호.PNG)}")
                # self.label3.setText(text_122)
            # 보통 양호
            elif (42 < upper_x <= 68) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/15보통보통양호.PNG)}")
                # self.label3.setText(text_112)
            # 양호 보통
            elif (upper_x > 68) and (42 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/17보통양호보통.PNG)}")
                # self.label3.setText(text_121)

        elif x > 68:
            y = (305 / 3 * 1) - ((x - 68) / 32 * (305 / 3))
            # self.label1.setText(text_good)
            # 심각 심각
            if (upper_x <= 42 and upper_x != 0) and (lower_x <= 42 and lower_x != 0):
                self.background.setStyleSheet("QLabel{background-image: url(resource/19양호심각심각.PNG)}")
                # self.label3.setText(text_200)
            # 보통 심각
            elif (42 < upper_x <= 68) and (lower_x <= 42 and lower_x != 0):
                self.background.setStyleSheet("QLabel{background-image: url(resource/22양호보통심각.PNG)}")
                # self.label3.setText(text_210)
            # 보통 보통
            elif (42 < upper_x <= 68) and (42 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/23양호보통보통.PNG)}")
                # self.label3.setText(text_211)
            # 심각 보통
            elif (upper_x <= 42 and upper_x != 0) and (42 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/20양호심각보통.PNG)}")
                # self.label3.setText(text_201)
            # 심각 양호
            elif (upper_x <= 42 and upper_x != 0) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/21양호심각양호.PNG)}")
                # self.label3.setText(text_202)
            # 양호 심각
            elif (upper_x > 68) and (lower_x <= 68 and lower_x != 0):
                self.background.setStyleSheet("QLabel{background-image: url(resource/25양호양호심각.PNG)}")
                # self.label3.setText(text_220)
            # 양호 양호
            elif (upper_x > 68) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/27양호양호양호.PNG)}")
                # self.label3.setText(text_222)
            # 보통 양호
            elif (42 < upper_x <= 68) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/24양호보통양호.PNG)}")
                # self.label3.setText(text_212)
            # 양호 보통
            elif (upper_x > 68) and (42 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/24양호양호보통.PNG)}")
                # self.label3.setText(text_221)

        self.graph_color_bar.setGeometry(QRect(79, 328, int(y), 38))
        self.graph_arrow.setGeometry(QRect(int((y + 79) - (39 / 2)), 323, 39, 80))

    def initUI(self):
        self.setWindowTitle('Tongue')

        self.background = QLabel(' ', self)
        self.background.setGeometry(QRect(0, 0, 467, 960))

        # self.move(700, 0)
        # self.resize(467, 960)

        # b1 = QPushButton('Detect Tongue', self)
        # b1.move(25, 18)
        # b1.clicked.connect(self.dialog_open)
        #
        # self.dialog = QDialog()

        # self.button = QPushButton('+', self)
        # self.button.clicked.connect(self.filedialog_open)
        # self.button.setGeometry(QRect(143, 130, 180, 180))
        # font = self.button.font()
        # font.setPointSize(50)
        # font.setBold(True)
        # self.button.setFont(font)
        self.label = QLabel(' ', self)
        self.label.setGeometry(QRect(143, 120, 180, 180))
        self.label.setStyleSheet("QLabel{background-image: url(tongue_result.jpg)}")

        self.graph_color_bar = QLabel(' ', self)
        self.graph_color_bar.setGeometry(QRect(79, 328, 305, 38))
        self.graph_color_bar.setStyleSheet("QLabel{background-image: url(resource/color_bar.png)}")

        self.graph_edge = QLabel(' ', self)
        self.graph_edge.setGeometry(QRect(74, 325, 317, 44))
        self.graph_edge.setStyleSheet("QLabel{background-image: url(resource/bar_edge.png)}")

        self.graph_arrow = QLabel(' ', self)
        self.graph_arrow.setGeometry(QRect(73, 323, 317, 44))
        self.graph_arrow.setStyleSheet("QLabel{background-image: url(resource/arrow.png)}")

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.refreshImage)
        self.timer.start()
        # self.button.move(180, 900)

        # self.b4 = QPushButton('나가기', self)
        self.b4 = QPushButton('다음', self)
        self.b4.move(345, 895)
        self.b4.clicked.connect(self.nextPage)

        self.b5 = QPushButton('이전', self)
        self.b5.move(22, 895)
        self.b5.clicked.connect(self.prevPage)

        self.title = QLabel('', self)
        self.title.setStyleSheet("QLabel{background-image: url(resource/결과요약.png)}")
        self.title.setGeometry(QRect(0, 0, 467, 76))

        # self.label = QLabel(self)
        # self.label.setStyleSheet("color: #000000; border-style: solid; border-width: 2px; border-color: "
        #                           "#080808; border-radius: 10px; ")
        # self.label.setGeometry(QRect(143, 130, 180, 180))

        # self.label1 = QLabel('진단 결과', self)
        # # self.label1.setStyleSheet("color: #000000; border-style: solid; border-width: 2px; border-color: "
        # #                           "#080808; border-radius: 10px; ")
        # self.label1.setGeometry(QRect(20, 310, 427, 90))
        # self.label1.setAlignment(Qt.AlignCenter)
        # font1 = self.label1.font()
        # font1.setPointSize(20)
        # font1.setBold(True)
        # self.label1.setFont(font1)
        # test_text = '백태 상태: 결과'
        # self.label1.setText(test_text)

        # self.label2 = QLabel('도움말', self)
        # self.label2.setGeometry(QRect(8, 760, 450, 50))
        # self.label2.setAlignment(Qt.AlignCenter)
        # font2 = self.label2.font()
        # font2.setPointSize(10)
        # self.label2.setFont(font2)
        # test_text = '* 증상이 완화되지 않고 너무 심하다면 병원을 방문하세요! *'
        # self.label2.setText(test_text)

        # self.label3 = QLabel('진단 결과', self)
        # # self.label3.setStyleSheet("color: #000000; border-style: solid; border-width: 2px; border-color: "
        # #                           "#080808; border-radius: 10px; ")
        # self.label3.setGeometry(QRect(20, 420, 430, 370))
        # self.label3.setAlignment(Qt.AlignTop)
        # font3 = self.label3.font()
        # font3.setPointSize(12)
        # self.label3.setFont(font3)
        # test_text = '자세한 진단 결과가 표시되는 영역입니다.'
        # # test_text = 'ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ'
        # self.label3.setText(test_text)
        #
        # self.label4 = QLabel('추천 사이트1', self)
        # self.label4.setGeometry(QRect(90, 790, 450, 50))
        # self.label4.setText('<a href="https://blog.naver.com/mohw2016/222838609558">보건복지부 블로그</a>')
        # self.label4.setOpenExternalLinks(True)
        #
        # self.label5 = QLabel('추천 사이트2', self)
        # self.label5.setGeometry(QRect(90, 815, 450, 50))
        # self.label5.setText('<a href="https://www.khealth.or.kr/kps/publish/view?menuId=MENU00891&page_no=B2017004&page'
        #                     'Num=1&siteId=&srch_text=%EA%B5%AC%EA%B0%95&srch_cate=&srch_type=ALL&str_clft_cd_list=&str_'
        #                     'clft_cd_type_list=&board_idx=10377">한국건강증진개발원 홍보자료</a>')
        # self.label5.setOpenExternalLinks(True)
        #
        # self.label6 = QLabel('추천 사이트3', self)
        # self.label6.setGeometry(QRect(90, 840, 450, 50))
        # self.label6.setText('<a href="https://mobile.hidoc.co.kr/healthstory/news/C0000641953">하이닥 백태관련 뉴스</a>')
        # self.label6.setOpenExternalLinks(True)

        # self.label4 = QLabel('진단 결과', self)
        # self.label4.setStyleSheet("color: #000000; border-style: solid; border-width: 2px; border-color: "
        #                           "#080808; border-radius: 10px; ")
        # self.label4.setGeometry(QRect(20, 570, 430, 150))
        # test_text = '혀의 하단부의 진단 결과가 표시되는 영역입니다.'
        #
        # self.label4.setText(test_text)

    # def changePage(self):
    #     widget.setCurrentIndex(widget.currentIndex() - 1)
    def nextPage(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def prevPage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)


class ResultPage2(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tongue')

        self.background = QLabel(' ', self)
        self.background.setGeometry(QRect(0, 0, 467, 960))

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.refreshImage)
        self.timer.start()

        self.b4 = QPushButton('다음', self)
        self.b4.move(345, 895)
        self.b4.clicked.connect(self.nextPage)

        self.b5 = QPushButton('이전', self)
        self.b5.move(22, 895)
        self.b5.clicked.connect(self.prevPage)

        self.title = QLabel('', self)
        self.title.setStyleSheet("QLabel{background-image: url(resource/전체결과.png)}")
        self.title.setGeometry(QRect(0, 0, 467, 76))

    def refreshImage(self):
        # 심각
        if x <= 42 and x != 0:
            self.background.setStyleSheet("QLabel{background-image: url(resource/1심각.PNG)}")
        # 보통
        elif 68 >= x > 42:
            self.background.setStyleSheet("QLabel{background-image: url(resource/2보통.PNG)}")
        # 양호
        elif x > 68:
            self.background.setStyleSheet("QLabel{background-image: url(resource/3양호.PNG)}")

    def nextPage(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def prevPage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)


class ResultPage3(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tongue')

        self.background = QLabel(' ', self)
        self.background.setGeometry(QRect(0, 0, 467, 960))

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.refreshImage)
        # self.timer.timeout.connect(self.nextPage)
        # self.timer.timeout.connect(self.prevPage)
        self.timer.start()
        # self.button.move(180, 900)

        self.b4 = QPushButton('다음', self)
        self.b4.move(345, 895)
        self.b4.clicked.connect(self.nextPage)

        self.b5 = QPushButton('이전', self)
        self.b5.move(22, 895)
        self.b5.clicked.connect(self.prevPage)

        self.title = QLabel('', self)
        self.title.setStyleSheet("QLabel{background-image: url(resource/세부결과.png)}")
        self.title.setGeometry(QRect(0, 0, 467, 76))

    def refreshImage(self):
        # 심각 심각
        if (upper_x <= 42 and upper_x != 0) and (lower_x <= 42 and lower_x != 0):
            self.background.setStyleSheet("QLabel{background-image: url(resource/1심각심각.PNG)}")
            # self.label3.setText(text_000)
        # 보통 심각
        elif (42 < upper_x <= 68) and (lower_x <= 42 and lower_x != 0):
            self.background.setStyleSheet("QLabel{background-image: url(resource/4보통심각.PNG)}")
            # self.label3.setText(text_010)
        # 보통 보통
        elif (42 < upper_x <= 68) and (42 < lower_x <= 68):
            self.background.setStyleSheet("QLabel{background-image: url(resource/5보통보통.PNG)}")
            # self.label3.setText(text_011)
        # 심각 보통
        elif (upper_x <= 42 and upper_x != 0) and (42 < lower_x <= 68):
            self.background.setStyleSheet("QLabel{background-image: url(resource/2심각보통.PNG)}")
            # self.background.setStyleSheet("QLabel{background-image: url(2페이지_임시4.PNG)}")
            # self.label3.setText(text_001)
        # 심각 양호
        elif (upper_x <= 42 and upper_x != 0) and (lower_x > 68):
            self.background.setStyleSheet("QLabel{background-image: url(resource/3심각양호.PNG)}")
            # self.label3.setText(text_002)
        # 양호 심각
        elif (upper_x > 68) and (lower_x <= 68 and lower_x != 0):
            self.background.setStyleSheet("QLabel{background-image: url(resource/7양호심각.PNG)}")
            # self.label3.setText(text_020)
        # 양호 양호
        elif (upper_x > 68) and (lower_x > 68):
            self.background.setStyleSheet("QLabel{background-image: url(resource/9양호양호.PNG)}")
            # self.label3.setText(text_022)
        # 보통 양호
        elif (42 < upper_x <= 68) and (lower_x > 68):
            self.background.setStyleSheet("QLabel{background-image: url(resource/6보통양호.PNG)}")
            # self.label3.setText(text_012)
        # 양호 보통
        elif (upper_x > 68) and (42 < lower_x <= 68):
            self.background.setStyleSheet("QLabel{background-image: url(resource/8양호보통.PNG)}")
            # self.label3.setText(text_021)

    def nextPage(self):
        if x > 68 or (upper_x > 68 and lower_x > 68):
            widget.setCurrentIndex(widget.currentIndex() + 2)
        else:
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def prevPage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)


class ResultPage4(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tongue')

        self.background = QLabel(' ', self)
        self.background.setGeometry(QRect(0, 0, 467, 960))

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.refreshImage)
        self.timer.start()
        # self.button.move(180, 900)

        self.b4 = QPushButton('다음', self)
        self.b4.move(345, 895)
        self.b4.clicked.connect(self.nextPage)

        self.b5 = QPushButton('이전', self)
        self.b5.move(22, 895)
        self.b5.clicked.connect(self.prevPage)

        self.title = QLabel('', self)
        self.title.setStyleSheet("QLabel{background-image: url(resource/권장식품.png)}")
        self.title.setGeometry(QRect(0, 0, 467, 76))

    def refreshImage(self):
        # 전체 양호가 아닌 경우
        if 68 > x > 0:
            # 소화계, 순환계
            if (0 < upper_x <= 68) and (0 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/소화계_순환계.PNG)}")
            # 양호 양호
            elif (upper_x > 68) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/18보통양호양호.PNG)}")
            # 소화계
            elif (0 < upper_x <= 68) and (lower_x > 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/소화계.PNG)}")
            # 순환계
            elif (upper_x > 68) and (0 < lower_x <= 68):
                self.background.setStyleSheet("QLabel{background-image: url(resource/순환계.PNG)}")

    def nextPage(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def prevPage(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)


class ResultPage5(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tongue')
        # self.move(700, 0)
        # self.resize(467, 960)

        self.background = QLabel('', self)
        self.background.setGeometry(QRect(0, 0, 467, 960))
        self.background.setStyleSheet("QLabel{background-image: url(resource/link_page.png)}")

        self.b4 = QPushButton('나가기', self)
        self.b4.move(345, 895)
        self.b4.clicked.connect(QCoreApplication.instance().quit)

        self.b5 = QPushButton('이전', self)
        self.b5.move(22, 895)
        self.b5.clicked.connect(self.prevPage)

        self.title = QLabel('', self)
        self.title.setStyleSheet("QLabel{background-image: url(resource/관련정보들.png)}")
        self.title.setGeometry(QRect(0, 0, 467, 76))

        self.button1 = QPushButton('', self)
        self.button1.setGeometry(QRect(68, 240, 44, 44))
        self.button1.setStyleSheet("QPushButton{background-image: url(resource/link_button.png)}")
        self.button1.clicked.connect(lambda: webbrowser.open('http://kowaent.co.kr/Module/News/Lecture.asp?Mode=V'
                                                             '&Srno=9044'))

        self.button2 = QPushButton('', self)
        self.button2.setGeometry(QRect(68, 360, 44, 44))
        self.button2.setStyleSheet("QPushButton{background-image: url(resource/link_button.png)}")
        self.button2.clicked.connect(lambda: webbrowser.open('https://blog.naver.com/witnvillage/222531086519'))

        self.button3 = QPushButton('', self)
        self.button3.setGeometry(QRect(68, 448, 44, 44))
        self.button3.setStyleSheet("QPushButton{background-image: url(resource/link_button.png)}")
        self.button3.clicked.connect(lambda: webbrowser.open('https://www.hidoc.co.kr/healthstory/news/C0000602256'))

        self.button4 = QPushButton('', self)
        self.button4.setGeometry(QRect(68, 597, 44, 44))
        self.button4.setStyleSheet("QPushButton{background-image: url(resource/link_button.png)}")
        self.button4.clicked.connect(lambda: webbrowser.open('https://mobile.hidoc.co.kr/healthstory/news/C0000641953'))

        self.button5 = QPushButton('', self)
        self.button5.setGeometry(QRect(68, 687, 44, 44))
        self.button5.setStyleSheet("QPushButton{background-image: url(resource/link_button.png)}")
        self.button5.clicked.connect(lambda: webbrowser.open('https://www.khealth.or.kr/kps/publish/view?menuId'
                                                             '=MENU00891&page_no=B2017004&pageNum=1&siteId=&srch_text'
                                                             '=%EA%B5%AC%EA%B0%95&srch_cate=&srch_type=ALL'
                                                             '&str_clft_cd_list=&str_clft_cd_type_list=&board_idx=10377'))

        self.button6 = QPushButton('', self)
        self.button6.setGeometry(QRect(68, 777, 44, 44))
        self.button6.setStyleSheet("QPushButton{background-image: url(resource/link_button.png)}")
        self.button6.clicked.connect(lambda: webbrowser.open('https://blog.naver.com/mohw2016/222838609558'))

    def prevPage(self):
        if x > 68 or (upper_x > 68 and lower_x > 68):
            widget.setCurrentIndex(widget.currentIndex() - 2)
        else:
            widget.setCurrentIndex(widget.currentIndex() - 1)


def homomorphic(img):
    img_YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y = img_YUV[:, :, 0]

    rows = y.shape[0]
    cols = y.shape[1]

    ### illumination elements와 reflectance elements를 분리하기 위해 log를 취함
    imgLog = np.log1p(np.array(y, dtype='float') / 255)  # y값을 0~1사이로 조정한 뒤 log(x+1)

    ### frequency를 이미지로 나타내면 4분면에 대칭적으로 나타나므로
    ### 4분면 중 하나에 이미지를 대응시키기 위해 row와 column을 2배씩 늘려줌
    M = 2 * rows + 1
    N = 2 * cols + 1

    ### gaussian mask 생성 sigma = 10
    sigma = 10
    (X, Y) = np.meshgrid(np.linspace(0, N - 1, N), np.linspace(0, M - 1, M))  # 0~N-1(and M-1) 까지 1단위로 space를 만듬
    Xc = np.ceil(N / 2)  # 올림 연산
    Yc = np.ceil(M / 2)
    gaussianNumerator = (X - Xc) ** 2 + (Y - Yc) ** 2  # 가우시안 분자 생성

    ### low pass filter와 high pass filter 생성
    LPF = np.exp(-gaussianNumerator / (2 * sigma * sigma))
    HPF = 1 - LPF

    ### LPF랑 HPF를 0이 가운데로 오도록iFFT함.
    ### 사실 이 부분이 잘 이해가 안 가는데 plt로 이미지를 띄워보니 shuffling을 수행한 효과가 났음
    ### 에너지를 각 귀퉁이로 모아 줌
    LPF_shift = np.fft.ifftshift(LPF.copy())
    HPF_shift = np.fft.ifftshift(HPF.copy())

    ### Log를 씌운 이미지를 FFT해서 LPF와 HPF를 곱해 LF성분과 HF성분을 나눔
    img_FFT = np.fft.fft2(imgLog.copy(), (M, N))
    img_LF = np.real(np.fft.ifft2(img_FFT.copy() * LPF_shift, (M, N)))  # low frequency 성분
    img_HF = np.real(np.fft.ifft2(img_FFT.copy() * HPF_shift, (M, N)))  # high frequency 성분

    ### 각 LF, HF 성분에 scaling factor를 곱해주어 조명값과 반사값을 조절함
    gamma1 = 0.3
    gamma2 = 1.5
    img_adjusting = gamma1 * img_LF[0:rows, 0:cols] + gamma2 * img_HF[0:rows, 0:cols]

    ### 조정된 데이터를 이제 exp 연산을 통해 이미지로 만들어줌
    img_exp = np.expm1(img_adjusting)  # exp(x) + 1
    img_exp = (img_exp - np.min(img_exp)) / (np.max(img_exp) - np.min(img_exp))  # 0~1사이로 정규화
    img_out = np.array(255 * img_exp, dtype='uint8')  # 255를 곱해서 intensity값을 만들어줌

    ### 마지막으로 YUV에서 Y space를 filtering된 이미지로 교체해주고 RGB space로 converting
    img_YUV[:, :, 0] = img_out
    result = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)
    return result


def recreate_image(codebook, labels, w, h):
    """Recreate the (compressed) image from the code book & labels"""
    d = codebook.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image


def meanshift(img):
    index = pd.MultiIndex.from_product((*map(range, img.shape[:2]), ('r', 'g', 'b')), names=('row', 'col', None))
    df_1 = pd.Series(img.flatten(), index=index)
    df_1 = df_1.unstack()
    df_1 = df_1.reset_index().reindex(columns=['col', 'row', 'r', 'g', 'b'])
    df_1.head(10)
    df_2 = df_1[['r', 'g', 'b']]

    nd_1 = df_2

    bandwidth_1 = estimate_bandwidth(nd_1, quantile=.01, n_jobs=-1)

    ms_1 = MeanShift(bandwidth=bandwidth_1, n_jobs=-1, bin_seeding=True, cluster_all=True).fit(nd_1)

    img_meanshift = recreate_image(ms_1.cluster_centers_[:, 2:], ms_1.labels_, img.shape[1], img.shape[0])
    # cv2.imshow("meanshift", img_meanshift)
    # cv2.waitKey()
    img_meanshift = img_meanshift.astype('uint8')
    # cv2.imshow("meanshift", img_meanshift)
    # cv2.waitKey()
    return img_meanshift


def tongue_detection(file_name):
    # 이미지 선택
    img_BGR = cv2.imread(file_name)

    # 이미지 비율 1:1로 조정
    if img_BGR.shape[0] > img_BGR.shape[1]:
        img_BGR = img_BGR[
                  int(img_BGR.shape[0] / 2 - img_BGR.shape[1] / 2):int(img_BGR.shape[0] / 2 + img_BGR.shape[1] / 2), :]
    elif img_BGR.shape[1] > img_BGR.shape[0]:
        img_BGR = img_BGR[:,
                  int(img_BGR.shape[1] / 2 - img_BGR.shape[0] / 2):int(img_BGR.shape[1] / 2 + img_BGR.shape[0] / 2)]
    else:
        pass

    # 이미지 크기 640 x 640으로 조정
    resize_img_640 = cv2.resize(img_BGR, (640, 640))
    my, mx = int(resize_img_640.shape[0] / 2), int(resize_img_640.shape[1] / 2)

    # # R, G, B 채널 분리
    # b, g, r = cv2.split(resize_img_640)
    #
    # # Red에 가깝지 않은 색 배제
    # for i in range(0, r.shape[0]):
    #     for j in range(0, r.shape[1]):
    #         if r[i][j] > g[i][j] and (r[i][j] - g[i][j]) > 10:
    #             pass
    #         else:
    #             r[i][j] = 0
    #             g[i][j] = 0
    #             b[i][j] = 0
    #
    # # 이미지 병합
    # img_merge_bgr = cv2.merge((b, g, r))
    # # cv2.imshow("img", img_merge_bgr)
    # # cv2.waitKey()

    # Homomorphic 이용 빛 영향 감소
    img_homomorphic = homomorphic(resize_img_640)

    # # BGR => HSV
    # img_hsv = cv2.cvtColor(img_homomorphic, cv2.COLOR_BGR2HSV)
    #
    # # H, s, v 채널 분리
    # h, s, v = cv2.split(img_hsv)
    #
    # # Red에 가깝지 않은 색 배제
    # for i in range(0, h.shape[0]):
    #     for j in range(0, h.shape[1]):
    #         if 20 < h[i][j] < 100:
    #             h[i][j] = 0
    #             s[i][j] = 0
    #             v[i][j] = 0
    #
    # # 이미지 병합
    # img_merge_hsv = cv2.merge((h, s, v))
    # img_hsv2bgr = cv2.cvtColor(img_merge_hsv, cv2.COLOR_HSV2BGR)
    # # cv2.imshow("img", img_hsv2bgr)
    # # cv2.waitKey()

    # 이미지 크기 축소
    img_small = cv2.resize(img_homomorphic, (120, 120))

    # Meanshift 이용하여 분할
    img_meanshift = meanshift(img_small)
    # cv2.imshow("meanshift", img_meanshift)
    # cv2.waitKey()

    # 스무딩
    smoothing_mask = np.array([[1 / 16, 1 / 8, 1 / 16], [1 / 8, 1 / 4, 1 / 8], [1 / 16, 1 / 8, 1 / 16]])
    img_smoothing = img_meanshift
    for i in range(0, 3):
        img_smoothing = cv2.filter2D(img_smoothing, -1, smoothing_mask)

    # Canny 에지 검출
    img_canny = cv2.Canny(img_smoothing, 5, 20)
    # cv2.imshow("canny", img_canny)
    # cv2.waitKey()

    # 팽창, 침식 연산
    img_canny = cv2.dilate(img_canny, kernel=(3, 3), iterations=5)
    img_canny = cv2.erode(img_canny, kernel=(1, 1), iterations=1)
    # cv2.imshow("canny", img_canny)
    # cv2.waitKey()

    # Canny 에지 검출 이미지 크기를 원본 이미지와 동일하게 조절
    img_canny_640 = cv2.resize(img_canny, (resize_img_640.shape[0], resize_img_640.shape[1]))

    # 침식연산으로 Canny 에지의 두께 감소
    # img_erode = cv2.erode(img_canny_640, kernel=(3, 3), iterations=1)

    # Canny 에지 기반 이미지 레이블링
    # img_neg = 255 - img_erode
    img_neg = 255 - img_canny_640
    # cv2.imshow("neg", img_neg)
    # cv2.waitKey()
    th, img_neg_bin = cv2.threshold(img_neg, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # print(th)
    for i in range(0, img_neg.shape[0]):
        for j in range(0, img_neg.shape[1]):
            if img_neg_bin[i][j] != 0:
                img_neg[i][j] = 255
            else:
                img_neg[i][j] = 0
    # cv2.imshow("neg", img_neg)
    # cv2.waitKey()

    # h기준 빨간색에 가까운 색만 남김
    img_hsv = cv2.cvtColor(img_homomorphic, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img_hsv)
    for i in range(0, h.shape[0]):
        for j in range(0, h.shape[1]):
            if 50 < h[i][j] < 140:
                h[i][j] = 0
                s[i][j] = 0
                v[i][j] = 0

    # cv2.imshow("img", h)
    # cv2.waitKey()

    # s값의 평균 구하기
    color_sum = 0
    color_count = 0
    for i in range(0, s.shape[0]):
        for j in range(0, s.shape[1]):
            if s[i][j] != 0:
                color_sum += s[i][j]
                color_count += 1
    mean = color_sum / color_count
    # print(mean)

    # s기준 이진화
    for i in range(0, s.shape[0]):
        for j in range(0, s.shape[1]):
            if s[i][j] < mean:
                h[i][j] = 0
                s[i][j] = 0
                v[i][j] = 0

    # cv2.imshow("img", h)
    # cv2.waitKey()

    # h값 평균 구하기 1
    color_sum = 0
    color_count = 0
    for i in range(0, h.shape[0]):
        for j in range(0, h.shape[1]):
            if h[i][j] != 0:
                color_sum += h[i][j]
                color_count += 1
    mean = color_sum / color_count
    # print(mean)

    # h기준 이진화 1
    for i in range(0, s.shape[0]):
        for j in range(0, s.shape[1]):
            # 결과물이 잘 나올 경우
            if mean > 20:
                if h[i][j] < mean:
                    h[i][j] = 0
                    s[i][j] = 0
                    v[i][j] = 0
            # 결과물이 별로일 경우
            else:
                if h[i][j] > mean:
                    h[i][j] = 0
                    s[i][j] = 0
                    v[i][j] = 0

    # h값 평균 구하기 2
    color_sum = 0
    color_count = 0
    for i in range(0, h.shape[0]):
        for j in range(0, h.shape[1]):
            if h[i][j] != 0:
                color_sum += h[i][j]
                color_count += 1
    mean = color_sum / color_count
    # print(mean)

    # cv2.imshow("img", h)
    # cv2.waitKey()

    # h기준 이진화 2
    if mean < 20:
        for i in range(0, s.shape[0]):
            for j in range(0, s.shape[1]):
                # 결과물이 별로일 경우
                if h[i][j] > mean:
                    h[i][j] = 0
                    s[i][j] = 0
                    v[i][j] = 0

    flag = 0
    # y축
    for j in range(0, h.shape[1]):
        for i in range(h.shape[0] - 1, 0, -1):
            if h[i][j] != 0 and flag != j:
                for m in range(i, 0, -1):
                    h[m][j] = mean
                    flag = j
            elif flag == j:
                break

    flag = 0
    # x축
    for i in range(0, h.shape[0]):
        for j in range(0, h.shape[1]):
            if h[i][j] != 0 and flag != i:
                for m in range(h.shape[1] - 1, j + 1, -1):
                    if h[i][m] != 0 and flag != i:
                        for n in range(j, m):
                            h[i][n] = mean
                            flag = i
                            # y_max_list.append(i)
                    elif flag == i:
                        break

    for i in range(0, h.shape[0]):
        for j in range(0, h.shape[1]):
            if img_neg[i][j] == 0:
                h[i][j] = 0

    # cv2.imshow("h", h)
    # cv2.waitKey()

    retval, labels = cv2.connectedComponents(h, labels=None, connectivity=8)
    label = np.empty((0, 0), int)
    for i in range(my - 50, my + 100):
        for j in range(mx - 100, mx + 100):
            if labels[i][j] != 0:
                label = np.append(label, labels[i][j])
    label = set(label)
    label = list(label)
    for i in range(0, img_neg.shape[0]):
        for j in range(0, img_neg.shape[1]):
            if labels[i][j] in label:
                labels[i][j] = 255
            else:
                labels[i][j] = 0
    # cv2.imshow("label", img_neg)
    # cv2.waitKey()

    # 이미지 개선
    flag = 0
    y_max_list = []

    # X축
    # for i in range(0, labels.shape[0]):
    #     for j in range(0, labels.shape[1]):
    #         if labels[i][j] != 0:
    #             x_min = j
    #             y_min = i
    #             for m in range(0, labels.shape[0]):
    #                 for n in range(labels.shape[1] - 1, 0, -1):
    #                     if labels[m][n] != 0:
    #                         x_max = n
    #                         y_max = m
    #                         if y_min == y_max:
    #                             for k in range(x_min, x_max):
    #                                 labels[y_min][k] = 1
    #                             flag = 1
    #                     if flag == 1:
    #                         break
    #                 if flag == 1:
    #                     break
    #         if flag == 1:
    #             flag = 0
    #             break
    for i in range(0, labels.shape[0]):
        for j in range(0, labels.shape[1]):
            if labels[i][j] != 0 and flag != i:
                for m in range(labels.shape[0] - 1, j + 1, -1):
                    if labels[i][m] != 0 and flag != i:
                        for n in range(j, m):
                            labels[i][n] = 1
                            flag = i
                            y_max_list.append(i)
                    elif flag == i:
                        break

    # Y축
    # for i in range(0, labels.shape[1]):
    #     for j in range(0, labels.shape[0]):
    #         if labels[j][i] != 0:
    #             x_min = i
    #             y_min = j
    #             for m in range(0, labels.shape[1]):
    #                 for n in range(labels.shape[0] - 1, 0, -1):
    #                     if labels[n][m] != 0:
    #                         x_max = m
    #                         y_max = n
    #                         if x_min == x_max:
    #                             for k in range(y_min, y_max):
    #                                 labels[k][x_min] = 1
    #                             flag = 1
    #                     if flag == 1:
    #                         break
    #                 if flag == 1:
    #                     break
    #         if flag == 1:
    #             flag = 0
    #             break
    for j in range(0, labels.shape[1]):
        for i in range(0, labels.shape[0]):
            if labels[i][j] != 0 and flag != j:
                for m in range(labels.shape[1] - 1, i + 1, -1):
                    if labels[m][j] != 0 and flag != j:
                        for n in range(i, m):
                            labels[n][j] = 1
                            flag = j
                    elif flag == j:
                        break

    # 혓바닥 영역 분할을 위한 기준점 찾기
    # y_max = 0
    y_max = min(y_max_list)
    y_min = 0

    # flag = 0
    # for i in range(0, labels.shape[0]):
    #     for j in range(0, labels.shape[1]):
    #         if labels[i][j] != 0:
    #             y_max = i
    #             flag = 1
    #             break
    #     if flag == 1:
    #         break

    flag = 0
    for i in range(labels.shape[0] - 1, 0, -1):
        for j in range(labels.shape[1] - 1, 0, -1):
            if labels[i][j] != 0:
                y_min = i
                flag = 1
                break
        if flag == 1:
            break

    height = y_min - y_max
    # print("height: ", height)
    line = y_min - int(height / 4)
    # print("line: ", line)

    # 레이블링을 Homomorphic 이미지에 적용
    img_detected = img_homomorphic.copy()
    for i in range(0, img_detected.shape[0]):
        for j in range(0, img_detected.shape[1]):
            if labels[i][j] == 0:
                img_detected[i][j] = 0
    # cv2.imshow("result", img_detected)
    # cv2.waitKey()

    # HSV를 통해 백태 검출
    hsv_result = cv2.cvtColor(img_detected, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_result)
    count = 0
    sum = 0

    # for i in range(0, s.shape[0]):
    #     for j in range(0, s.shape[1]):
    #         if s[i][j] != 0:
    #             count += 1
    #             sum += s[i][j]
    #
    # mean = sum / count
    #
    # for i in range(0, s.shape[0]):
    #     for j in range(0, s.shape[1]):
    #         if s[i][j] < mean and s[i][j] != 0:
    #             hsv_result[i][j][0] = 346
    #             hsv_result[i][j][1] = 96
    #             hsv_result[i][j][2] = 93
    #         elif s[i][j] > mean:
    #             hsv_result[i][j][0] = 0
    #             hsv_result[i][j][1] = 0
    #             hsv_result[i][j][2] = 105
    for i in range(0, s.shape[0]):
        for j in range(0, s.shape[1]):
            if s[i][j] != 0:
                count += 1
                sum += s[i][j]

    mean = sum / count

    count1 = 0
    sum1 = 0
    count2 = 0
    sum2 = 0

    count3 = 0
    sum3 = 0
    count4 = 0
    sum4 = 0

    for i in range(0, s.shape[0]):
        for j in range(0, s.shape[1]):
            if s[i][j] < mean and s[i][j] != 0:
                resize_img_640[i][j][0] = 255
                resize_img_640[i][j][1] = 255
                resize_img_640[i][j][2] = 255
                sum1 += s[i][j]
                count1 += 1
                if i > line:
                    sum3 += s[i][j]
                    count3 += 1

            elif s[i][j] > mean:
                resize_img_640[i][j][0] = 0
                resize_img_640[i][j][1] = 0
                resize_img_640[i][j][2] = 255
                sum2 += s[i][j]
                count2 += 1
                if i > line:
                    sum4 += s[i][j]
                    count4 += 1

    mean1 = sum1 / count1
    mean2 = sum2 / count2
    # substract = mean2 - mean1
    divide = mean1 / mean2 * 100
    # print(mean1, mean2, "\n", substract, divide)
    # ratio1 = (sum3 / count3) / (sum4 / count4) * 100
    # ratio2 = ((sum1 - sum3) / (count1 - count3)) / ((sum2 - sum4) / (count2 - count4)) * 100
    ratio1 = (sum3 / count3) / mean2 * 100
    ratio2 = ((sum1 - sum3) / (count1 - count3)) / mean2 * 100
    # print(divide, ratio1, ratio2)
    # 혓바닥 영역 분할 라인 그리기
    for i in range(0, resize_img_640.shape[0]):
        for j in range(0, resize_img_640.shape[1]):
            if i == line:
                resize_img_640[i][j][0] = 255
                resize_img_640[i][j][1] = 255
                resize_img_640[i][j][2] = 0

    # cv2.imshow('img', resize_img_640)
    # cv2.waitKey()
    resize_img_180 = cv2.resize(resize_img_640, (180, 180))
    cv2.imwrite('tongue_result.jpg', resize_img_180)
    global x
    x = divide
    global lower_x
    lower_x = ratio1
    global upper_x
    upper_x = ratio2
    print("전체 백태: ", x, "\n상단 백태: ", upper_x, "\n하단 백태: ", lower_x)
    # return divide, ratio1, ratio2
    # hsv_result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
    # cv2.imshow("sat_bin", resize_img_640)
    # cv2.waitKey()

    # b, g, r = cv2.split(resize_img_640)
    # count = 0
    # sum = 0
    #
    # for i in range(0, r.shape[0]):
    #     for j in range(0, r.shape[1]):
    #         if r[i][j] != 0:
    #             count += 1
    #             sum += r[i][j]
    #
    # mean = sum / count
    #
    # for i in range(0, r.shape[0]):
    #     for j in range(0, r.shape[1]):
    #         if r[i][j] < mean and r[i][j] != 0:
    #             resize_img_640[i][j][0] = 0
    #             resize_img_640[i][j][1] = 0
    #             resize_img_640[i][j][2] = 255
    #         elif r[i][j] > mean:
    #             resize_img_640[i][j][0] = 0
    #             resize_img_640[i][j][1] = 255
    #             resize_img_640[i][j][2] = 0
    # cv2.imshow("bin", resize_img_640)
    # cv2.waitKey()

    # plt.figure(figsize=(4, 4))
    # plt.subplot(1, 2, 1)
    # plt.imshow(img_BGR)
    # plt.axis('off')
    # plt.title('Image')
    # # plt.subplot(1, 3, 2)
    # # plt.imshow(cv2.cvtColor(img_detected, cv2.COLOR_BGR2RGB))
    # # plt.axis('off')
    # # plt.title('Tongue')
    # plt.subplot(1, 2, 2)
    # plt.imshow(cv2.cvtColor(resize_img_640, cv2.COLOR_BGR2RGB))
    # plt.axis('off')
    # plt.title('Result')
    # plt.subplot(1, 4, 1)
    # plt.axis('off')
    # plt.title('Description: ')
    # # plt.subplot(1, 4, 4)
    # # plt.imshow(resize_img)
    # # plt.axis('off')
    # # plt.title('resize_img')
    # plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    ex = TitlePage()
    ex2 = AnalyzePage()
    ex3 = ResultPage()
    ex4 = ResultPage2()
    ex5 = ResultPage3()
    ex6 = ResultPage4()
    ex7 = ResultPage5()
    widget.addWidget(ex)
    widget.addWidget(ex2)
    widget.addWidget(ex3)
    widget.addWidget(ex4)
    widget.addWidget(ex5)
    widget.addWidget(ex6)
    widget.addWidget(ex7)
    widget.setFixedHeight(960)
    widget.setFixedWidth(467)
    widget.show()
    sys.exit(app.exec_())
