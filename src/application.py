from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import os, sys, cv2 as cv

from canvas import *

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
        self.button.clicked.connect(self.load_clicked)
        self.label = QLabel(self)
        self.show()

    @pyqtSlot()
    def load_clicked(self):
        base_path= os.path.dirname(os.path.dirname(__file__))
        fname = 'black_50_50.png'
        if fname:
            self.load_image(os.path.join(base_path, 'misc', fname))
        else:
            raise FileNotFoundError('The image ' + image + ' does not exist')
    
    def load_image(self, fname):
        self.image = cv.imread(fname, cv.IMREAD_COLOR)
        self.display_image()

    def display_image(self):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if(self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
            img = QImage(self.image, self.image.shape[1], self.image.shape[0], qformat)
            img = img.rgbSwapped()
            self.spares.append(img)
            self.index += 1
            self.label.setPixmap(QPixmap.fromImage(img))
            self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)