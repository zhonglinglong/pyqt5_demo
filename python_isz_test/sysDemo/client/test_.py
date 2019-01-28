from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTabWidget, QPushButton, \
    QVBoxLayout, QHBoxLayout, QWidget, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem, QTabBar
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaMetaData, QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow):
    """docstring for MainWindow"""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        gridlayout = QGridLayout(self.centralwidget)

        hlayout = QHBoxLayout()
        self.button1 = QPushButton(' add image ')
        self.button3 = QPushButton('add video')
        self.button2 = QPushButton('remove')
        self.playbutton = QPushButton('play')
        self.stopbutton = QPushButton('stop')

        hlayout.addWidget(self.button1)
        hlayout.addWidget(self.button3)
        hlayout.addWidget(self.button2)
        hlayout.addWidget(self.playbutton)
        hlayout.addWidget(self.stopbutton)

        self.scene = QGraphicsScene()
        self.item = QGraphicsPixmapItem()

        imgpath = 'C:\\Users\Administrator\Pictures\Saved Pictures\\1.jpg'
        self.item.setPixmap(QtGui.QPixmap(imgpath))
        self.scene.addItem(self.item)
        self.graphicsview = QGraphicsView()
        self.graphicsview.setScene(self.scene)
        self.tabwidget = QTabWidget()

        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.tabwidget)

        MainWindow.setCentralWidget(self.centralwidget)
        gridlayout.addLayout(vlayout, 0, 0, 1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.button1.clicked.connect(self.addTab)
        self.button2.clicked.connect(self.closeTab)
        self.button3.clicked.connect(self.addVideo)
        self.playbutton.clicked.connect(self.palyMedia)
        self.stopbutton.clicked.connect(self.stopMedia)
        pass

    def addTab(self, signal):
        scene = QGraphicsScene()
        item = QGraphicsPixmapItem()
        # imgpath = 'C:/Users/liesmars/Desktop/1.jpg'

        item.setPixmap(QtGui.QPixmap(imgpath))
        scene.addItem(item)
        graphicsview = QGraphicsView()
        graphicsview.setScene(scene)
        self.tabwidget.addTab(graphicsview, "tab2")
        self.tabwidget.setCurrentWidget(graphicsview)

    def addVideo(self, signal):
        videowidget = QVideoWidget()
        self.videoplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoplayer.setVideoOutput(videowidget)
        # videopath = 'C:/Users/liesmars/Desktop/1.mp4'
        self.videoplayer.setMedia(QMediaContent(QUrl.fromLocalFile(videopath)))

        self.tabwidget.addTab(videowidget, "tab4")
        self.tabwidget.setCurrentWidget(videowidget)

    def closeTab(self):
        tabID = self.tabwidget.currentIndex()
        self.tabwidget.removeTab(tabID)
        pass

    def palyMedia(self, signal):
        self.videoplayer.play()
        pass

    def stopMedia(self, signal):
        self.videoplayer.pause()
        pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    # app.setActiveWindow(mainWin)
    mainWin.show()
    sys.exit(app.exec_())

