from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import math
import functions

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
        self.images = []
        self.index = -1
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        #m = PlotCanvas(self, width=5, height=4)
        #m.move(0,0)
        

        self.btn_add_image = QPushButton('Ajouter une image', self)
        self.btn_add_image.setToolTip('cliquer pour ajouter une premiere image')
        self.btn_add_image.move(500, 0)
        self.btn_add_image.resize(140, 100)
        self.btn_add_image.clicked.connect(self.load_clicked)

        self.btn_process = QPushButton('Go', self)
        self.btn_process.setToolTip('cliquer pour effectuer un tracé de bresenham')
        self.btn_process.move(500, 110)
        self.btn_process.resize(140, 100)
        #self.btn_process.clicked.connect(self.process_test)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(359)
        self.slider.setSingleStep(1)
        self.slider.move(0, 300)
        self.slider.resize(360, 20)

        self.slider.valueChanged.connect(self.process_test)

        #self.image1 = QLabel(self)
        #self.image2 = QLabel(self)
        self.show()

    @pyqtSlot()
    def load_clicked(self):
        base_path= os.path.dirname(os.path.dirname(__file__))
        fname = 'black_50_50.png'
        if fname:
            self.load_image(os.path.join(base_path, 'misc', fname))
        else:
            raise FileNotFoundError('The image ' + image + ' does not exist')
    
    '''
    Reads and image with OpenCV & displays it with self.display_image()
    '''
    def load_image(self, fname):
        self.images.append(cv.imread(fname, cv.IMREAD_COLOR))
        self.index += 1
        self.display_image()
        
    '''
    Creates an ImageCanvas & moves it to the origin (0,0)
    '''
    def display_image(self):
        self.image1 = ImageCanvas(self, width = 2, height = 2)
        self.image1.move(0, 0)

    @pyqtSlot()
    def process_test(self):
        """
        create all the segments giving and test scan parralels
        test if each pixel is contained in one of the segments, only once
        """
        
        degree = self.slider.value()
        angle = (degree /180)* math.pi
        if len(self.images) >0:
            height, width = self.images[0].shape
            diag = math.sqrt(2 * height^2)
            x = diag * math.cos(angle)
            y = diag * math.sin(angle)
            print(x, y)
            #seg = functions.get_segment(0, 0, x, y, height)
            #functions.print_segment(seg, height)
            #segs = functions.scan_parrallel(seg, height)
        #print(functions.test_segments(segs, height))
        #passed_all = functions.test_all_segments(height)
        #print("worked with all segment :", passed_all)
    
    def generate_image(self, size):
        self.image1 = np.zeros((size, size, 3), dtype="uint8")
