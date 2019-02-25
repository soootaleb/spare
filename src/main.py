"""
SpaRe
Projet de TER Taleb Sofiane et Doisneau Gabriel : Spacial Recognition
"""
import matplotlib
import cv2 as cv
import random, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import(QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy,
    QMessageBox, QWidget, QPushButton, QFileDialog, QLabel)
from PyQt5.QtGui import QIcon

# We need to change the used backend to not rely on the system one
matplotlib.use('Qt5Agg')

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.title = 'SpaRe'
        self.width = 640
        self.height = 400
        self.spares = []
        self.index = -1
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)
 
        self.button = QPushButton('Ajouter une image', self)
        self.button.setToolTip('cliquer pour ajouter la premiere image')
        self.button.move(500, 0)
        self.button.resize(140, 100)
        self.button.clicked.connect(self.loadClicked)
        self.label = QLabel(self)
        self.show()

    @pyqtSlot()
    def loadClicked(self):
        base_path=".\misc"
        #fname, filter = QFileDialog.getOpenFileName(self, 'Open File', base_path, "Image Files(*.jpg, *.png)")
        fname = "./misc/black_50_50.png"
        if fname:
            self.loadImage(fname)
        else:
            print('invalid image')
    
    def loadImage(self,fname):
        self.image = cv.imread(fname, cv.IMREAD_GRAYSCALE)
        self.displayImage()
        
    def displayImage(self):
        qformat = QImage.Format_Indexed8
        print(self.image.shape)
        print(self.image.strides)
        if len(self.image.shape) == 3:
            if(self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
            img = QImage(self.image, self.image.shape[1], self.image.shape[0], qformat)
            img = img.rgbSwapped()
            print(self.image.shape[1], self.image.shape[0], self.image.strides[0])
            self.spares.append(img)
            self.index += 1
            self.label.setPixmap(QPixmap.fromImage(img))
            #self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())