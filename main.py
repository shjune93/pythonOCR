## Ex 3-7. 툴바 만들기.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QLabel, QTextEdit, QHBoxLayout,QPushButton,QVBoxLayout,QWidget,QComboBox
from PyQt5.QtGui import QIcon
import pyperclip
import cv2 as cv
from PIL import ImageGrab
import pytesseract

#마우스 좌표받아서 처리하는 함수
isDragging = False
x1,y1,x2,y2 = -1,-1,-1,-1
blue,red = (255,0,0),(0,0,255)
global tb


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        tb = TextBox()
        language = tb.cb.currentText()

        #캡쳐 툴바
        capAction = QAction(QIcon('./img/edit.png'), 'Edit', self)
        capAction.setShortcut('Ctrl+W')
        capAction.setStatusTip('Capture application')
        capAction.triggered.connect(lambda action:capture())
        #ocr툴바
        ocrAction = QAction(QIcon('./img/print.png'), 'OCR', self)
        ocrAction.setShortcut('Ctrl+E')
        ocrAction.setStatusTip('OCR application')
        ocrAction.triggered.connect(lambda action: tb.setTexts(pytesseract.image_to_string(cv.imread('./save.jpg'), lang=tb.cb.currentText())))
        #종료툴바
        exitAction = QAction(QIcon('./img/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)


        #툴바생성
        self.statusBar()
        #툴바에 추가
        self.toolbar = self.addToolBar('Capture')
        self.toolbar.addAction(capAction)

        self.toolbar = self.addToolBar('OCR')
        self.toolbar.addAction(ocrAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)





        #텍스트박스 생성
        self.setCentralWidget(tb)


        self.setWindowTitle('QTextEdit')
        self.setGeometry(1620, 840, 300, 200)
        self.show()

        def onMouse(event, x, y, flags, param):
            global isDragging, x1, y1
            if event == cv.EVENT_LBUTTONDOWN:  # 왼쪽마우스버튼 눌렀을때
                isDragging = True
                x1 = x
                y1 = y
            elif event == cv.EVENT_MOUSEMOVE:  # 움직일때
                if isDragging:
                    img_draw = img.copy()
                    # 영역표시
                    cv.rectangle(img_draw, (x1, y1), (x, y), blue, 2)
                    cv.imshow('img', img_draw)
            elif event == cv.EVENT_LBUTTONUP:  # 왼쪽 마우스버튼 땟을때
                if isDragging:
                    isDragging = False
                    x2 = x
                    y2 = y
                    print('x:%d, y%d,w:%d,h:%d' % (x1, y1, x2, y2))

                    img_draw = img.copy()
                    # 영역표시
                    cv.rectangle(img_draw, (x1, y1), (x2, y2), red, 2)
                    cv.imshow('img', img_draw)
                    # 우->좌 ,하 ->상으로 드래그시 수정
                    if x1 > x2:
                        x1, x2 = x2, x1
                    if y1 > y2:
                        y1, y2 = y2, y1

                    roi = img[y1:y2, x1:x2]
                    # 영역보여주기
                    #cv.imshow('capture', roi)
                    # cv.moveWindow('cropped',0,0)
                    # 파일저장
                    # tb.setTexts=pytesseract.image_to_string(cv.imread('./save.jpg'), lang='kor')
                    cv.imwrite('./save.jpg', roi)
                    print('capture')

                    #창 활성화
                    self.activateWindow()
                    #글자추출할 언어받아오기 kor,eng,kor+eng
                    language=tb.cb.currentText()
                    # 글자추출
                    tb.setTexts(pytesseract.image_to_string(cv.imread('./save.jpg'), lang=language))
                    #cv.destroyAllWindows()


        def capture():
            # 스크린샷 찍고저장
            global img
            cv.destroyAllWindows()
            img = ImageGrab.grab()
            img.save('./screenshot.jpg')

            # 찍은 스크린샷 불러오기
            img = cv.imread('./screenshot.jpg', cv.IMREAD_COLOR)
            #타이틀바 없애보기
            #https://stackoverflow.com/questions/49095446/python-opencv-remove-title-bar-toolbar-and-status-bar
            cv.namedWindow('img', cv.WND_PROP_FULLSCREEN)
            cv.setWindowProperty('img', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

            cv.imshow('img', img)
            cv.setMouseCallback('img', onMouse)
            cv.waitKey()
            cv.destroyAllWindows()



class TextBox(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl1 = QLabel('Enter your sentence:')

        self.te = QTextEdit()
        self.te.setAcceptRichText(False)

        self.lbl2 = QLabel('The number of words is 0')

        self.cb=QComboBox(self)
        self.cb.addItem('kor')
        self.cb.addItem('eng')
        self.cb.addItem('kor+eng')


        self.bt=QPushButton('클립보드 복사',self)


        self.te.textChanged.connect(self.text_changed)

        hbox=QHBoxLayout()
        hbox.addWidget(self.bt)
        hbox.addWidget(self.cb)


        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.te)
        vbox.addWidget(self.lbl2)
        vbox.addLayout(hbox)

        vbox.addStretch()


        self.setLayout(vbox)

        #self.cb.activated[str].connect(self.onActivated)
        self.bt.clicked.connect(self.getText)

        self.setWindowTitle('QTextEdit')
        self.setGeometry(300, 300, 300, 200)
        self.show()



    def setTexts(self,text):
        self.te.setText(text)
    def text_changed(self):
        text = self.te.toPlainText()
        self.lbl2.setText('The number of words is ' + str(len(text.split())))
    def getText(self):
        pyperclip.copy(self.te.toPlainText())
        cv.destroyAllWindows()
    # def onActivated(self,text):
    #     print(text)
    #     self.te.setTexts(pytesseract.image_to_string(cv.imread('./save.jpg'), lang=text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())



