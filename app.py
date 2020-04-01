# coding:utf-8
import sys
import os
import base64
import requests
import json
import PyQt5.QtGui
import PyQt5.QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt
from PIL import ImageGrab
import pyperclip
import matplotlib.pyplot as plt

env = os.environ

default_headers = {
    'app_id': env.get('APP_ID', '你的APP_ID'),
    'app_key': env.get('APP_KEY', '你的APP_KEY'),
    'Content-type': 'application/json'
}

service = 'https://api.mathpix.com/v3/latex'

class Img2Latex(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 700)
        self.setWindowTitle('Img2Latex')

        # copy latex
        self.Latex1copyBtn = QPushButton()
        self.Latex2copyBtn = QPushButton()
        self.Latex3copyBtn = QPushButton()
        # set copy btn icon
        self.Latex1copyBtn.setIcon(PyQt5.QtGui.QIcon(r".\img\copy.png"))
        self.Latex2copyBtn.setIcon(PyQt5.QtGui.QIcon(r".\img\copy.png"))
        self.Latex3copyBtn.setIcon(PyQt5.QtGui.QIcon(r".\img\copy.png"))

        # edit latex
        self.Latex1EditBtn = QPushButton()
        self.Latex2EditBtn = QPushButton()
        self.Latex3EditBtn = QPushButton()
        # set edit btn icon
        self.Latex1EditBtn.setIcon(PyQt5.QtGui.QIcon(r".\img\edit.png"))
        self.Latex2EditBtn.setIcon(PyQt5.QtGui.QIcon(r".\img\edit.png"))
        self.Latex3EditBtn.setIcon(PyQt5.QtGui.QIcon(r".\img\edit.png"))

        # img to latex convert btn
        self.img2latexBtn = QPushButton('convert')

        # show the picture on clipboard
        self.imgLable = QLabel()

        # show the formula in latex
        self.Latex1Edit = QLineEdit()
        self.Latex2Edit = QLineEdit()
        self.Latex3Edit = QLineEdit()
        self.Latex1Edit.setEnabled(False)
        self.Latex2Edit.setEnabled(False)
        self.Latex3Edit.setEnabled(False)

        # # show the convert latex result
        # self.reviewImgLable = QLabel()
        # self.reviewImgLable.setStyleSheet("border: 2px solid red")

        grid = QGridLayout()
        grid.setSpacing(20)

        # 排版
        grid.addWidget(self.imgLable, 1, 0, 5, 3)

        grid.addWidget(self.img2latexBtn,6,0,1,2)

        grid.addWidget(self.Latex1Edit, 7, 0)
        grid.addWidget(self.Latex1copyBtn, 7, 1)
        # grid.addWidget(self.Latex1EditBtn, 7, 2)

        grid.addWidget(self.Latex2copyBtn, 8, 1)
        grid.addWidget(self.Latex2Edit, 8, 0)
        # grid.addWidget(self.Latex2EditBtn, 8, 2)

        grid.addWidget(self.Latex3copyBtn, 9, 1)
        grid.addWidget(self.Latex3Edit, 9, 0)
        # grid.addWidget(self.Latex3EditBtn, 9, 2)

        # grid.addWidget(self.reviewImgLable, 10, 0, 4, 3)

        self.setLayout(grid)

        # sign and slot

        # img to latex convert
        self.img2latexBtn.clicked.connect(self.convert)

        # copy latex
        self.Latex1copyBtn.clicked.connect(self.copyLatex1)
        self.Latex2copyBtn.clicked.connect(self.copyLatex2)
        self.Latex3copyBtn.clicked.connect(self.copyLatex3)

        # edit latex
        # self.Latex1EditBtn.clicked.connect(self.Latex1EditImg)
        # self.Latex1Edit.textChanged.connect(self.Latex1EditImg)

        # self.Latex2EditBtn.clicked.connect(self.Latex2EditImg)
        # self.Latex2Edit.textChanged.connect(self.Latex2EditImg)

        # self.Latex3EditBtn.clicked.connect(self.Latex3EditImg)
        # self.Latex3Edit.textChanged.connect(self.Latex3EditImg)

        # beautify the window
        self.Beautify()
        self.show()

    def Beautify(self):
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(qtpy.QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        # self.setWindowFlag(qtpy.QtCore.Qt.FramelessWindowHint) # 隐藏边框
        pe = PyQt5.QtGui.QPalette()
        self.setAutoFillBackground(True)
        # pe.setColor(PyQt5.QtGui.QPalette.Window, Qt.Black)  #设置背景色
        pe.setColor(PyQt5.QtGui.QPalette.Background, Qt.black)
        self.setPalette(pe)
        self.imgLable.setStyleSheet(
            ''' QLabel{
                border: 2px solid red;
                border-radius:15px;
                padding:2px 4px;
                background-color:#aaa;
            }''')
        # self.reviewImgLable.setStyleSheet(
        #     ''' QLabel{
        #         border: 2px solid red;
        #         border-radius:15px;
        #         padding:2px 4px;
        #         background-color:#aaa;
        #
        #     }''')
        self.Latex1Edit.setStyleSheet(
            '''QLineEdit{
                border:1px solid gray;
                border-radius:10px;
                padding:2px 4px;
                background-color:#ddd;
                height:35px;
                font-color:black;
                font-weight:1000;
                font-size:24px
            }''')
        self.Latex2Edit.setStyleSheet(
            '''QLineEdit{
                border:1px solid gray;
                border-radius:10px;
                padding:2px 4px;
                background-color:#ddd;
                height:35px;
                font-color:black;
                font-weight:1000;
                font-size:24px
            }''')
        self.Latex3Edit.setStyleSheet(
            '''QLineEdit{
                border:1px solid gray;
                border-radius:10px;
                padding:2px 4px;
                background-color:#ddd;
                height:35px;
                font-color:black;
                font-weight:1000;
                font-size:24px
            }''')

        self.Latex1copyBtn.setStyleSheet(
            '''QPushButton{
                border:1px solid gray;
                border-radius:4px;
                padding:5px 5px;
                height:35px

            }''')
        self.Latex2copyBtn.setStyleSheet(
            '''QPushButton{
                border:1px solid gray;
                border-radius:4px;
                padding:5px 5px;
                height:35px
            }''')
        self.Latex3copyBtn.setStyleSheet(
            '''QPushButton{
                border:1px solid gray;
                border-radius:4px;
                padding:5px 5px;
                height:35px
            }''')
        # self.Latex1EditBtn.setStyleSheet(
        #     '''QPushButton{
        #         border:1px solid gray;
        #         border-radius:4px;
        #         padding:5px 5px;
        #         height:35px
        #     }''')
        # self.Latex2EditBtn.setStyleSheet(
        #     '''QPushButton{
        #         border:1px solid gray;
        #         border-radius:4px;
        #         padding:5px 5px;
        #         height:35px
        #     }''')
        # self.Latex3EditBtn.setStyleSheet(
        #     '''QPushButton{
        #         border:1px solid gray;
        #         border-radius:4px;
        #         padding:5px 5px;
        #         height:35px
        #     }''')

        self.img2latexBtn.setStyleSheet(
            '''QPushButton{
                border:2px solid gray;
                border-radius:10px;
                padding:5px 5px;
                background-color:#555;
                font-size:24px;
                font-color:#fff;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }''')

    #
    # Return the base64 encoding of an image with the given filename.
    #

    def image_uri(self,filename):
        image_data = open(filename, "rb").read()
        return "data:image/jpg;base64," + base64.b64encode(image_data).decode()

    # Call the Mathpix service with the given arguments, headers, and timeout.
    def latex(self,args, headers=default_headers, timeout=30):
        r = requests.post(service,
                          data=json.dumps(args), headers=headers, timeout=timeout)
        return json.loads(r.text)

    def convert(self):
        self.grabclipboard()
        r = self.latex({
            'src':self.image_uri(r".\img\equa.png"),
            'formats': ['latex_simplified']
        })
        # print(r['latex_simplified'])
        latex1 = r['latex_simplified']

        # test
        # latex1='111'
        latex2 = '$' + latex1 + '$'
        latex3 = '$$' + latex1 + '$$'
        self.Latex1Edit.setText(latex1)
        self.Latex2Edit.setText(latex2)
        self.Latex3Edit.setText(latex3)

    def copyLatex1(self):
        # get the latex formula
        text = self.Latex1Edit.text()
        # copy it to clipboard
        pyperclip.copy(text)

    def copyLatex2(self):
        text = self.Latex2Edit.text()
        pyperclip.copy(text)

    def copyLatex3(self):
        text = self.Latex3Edit.text()
        pyperclip.copy(text)

    #
    # latex to img
    #

    # def reviewImg(self,txt):
    #     txt2 = '$$'+txt+'$$'
    #     # use plt to show latex on picture
    #
    #     fig = plt.gcf()
    #     fig.set_size_inches(15.0 / 3, 2.5 / 3)
    #     # Refresh picture
    #     new_fig = plt.gcf()
    #     new_fig.set_size_inches(15.0 / 3, 2.5 / 3)
    #
    #     # 隐藏横纵坐标
    #     plt.axis('off')
    #     plt.text(0,0.5,'',fontsize=5)
    #     new_fig.savefig(r'.\img\reviewLatex.png', format='png', transparent=True, dpi=300, pad_inches=5)
    #     plt.show()
    #
    #     plt.axis('off')
    #     plt.text(0,0.5,txt2, fontsize=5)
    #
    #     fig.savefig(r'.\img\reviewLatex.png', format='png', transparent=True, dpi=300, pad_inches=5)
    #     plt.show()
    #     # show it on reviewImgLabel
    #     self.reviewImgLable.setPixmap(PyQt5.QtGui.QPixmap(r'.\img\reviewLatex.png'))


    # def Latex1EditImg(self):
    #     text = self.Latex1Edit.text()
    #     text2 = '$' + text + '$'
    #     text3 = '$$' + text + '$$'
    #     self.Latex2Edit.setText(text2)
    #     self.Latex3Edit.setText(text3)
    #
    #     if(text != ''):
    #         self.reviewImg(text)
    #     else:
    #         self.reviewImgLable.setPixmap(PyQt5.QtGui.QPixmap(r'.\img\error.png'))
    #
    # def Latex2EditImg(self):
    #     text = self.Latex2Edit.text()
    #     text2 = text[1:len(text)-1]
    #     text3 = '$' + text + '$'
    #     self.Latex1Edit.setText(text2)
    #     self.Latex3Edit.setText(text3)
    #     if(text != ''):
    #         self.reviewImg(text2)
    #     else:
    #         self.reviewImgLable.setPixmap(PyQt5.QtGui.QPixmap(r'.\img\error.png'))
    #
    # def Latex3EditImg(self):
    #     text = self.Latex3Edit.text()
    #     text2 = text[2:len(text) - 2]
    #     text3 = text[1:len(text) - 1]
    #     self.Latex1Edit.setText(text2)
    #     self.Latex2Edit.setText(text3)
    #     if(text != ''):
    #         self.reviewImg(text2)
    #     else:
    #         self.reviewImgLable.setPixmap(PyQt5.QtGui.QPixmap(r'.\img\error.png'))

    #
    # 识别剪贴板公式
    #
    def grapclipboard(self):
        im = ImageGrab.grabclipboard()
        im.save(r'.\img\equa.png', 'PNG')
        self.imgLable.setPixmap(PyQt5.QtGui.QPixmap(r'.\img\equa.png'))

    #
    # 为程序添加快捷键
    #

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_T)and(event.modifiers() == Qt.AltModifier):
            self.convert()
        if (event.key() == Qt.Key_C)and(event.modifiers() == Qt.AltModifier):
            self.copyLatex3()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Img2Latex()
    sys.exit(app.exec_())