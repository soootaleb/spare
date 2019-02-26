from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
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
 
        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)
 
        self.btn_add_image = QPushButton('Ajouter une image', self)
        self.btn_add_image.setToolTip('cliquer pour ajouter une premiere image')
        self.btn_add_image.move(500, 0)
        self.btn_add_image.resize(140, 100)
        self.btn_add_image.clicked.connect(self.load_clicked)

        self.btn_process = QPushButton('Go', self)
        self.btn_process.setToolTip('cliquer pour effectuer un tracé de bresenham')
        self.btn_process.move(500, 110)
        self.btn_process.resize(140, 100)
        self.btn_process.clicked.connect(self.process_test)


        self.image1 = QLabel(self)
        self.image2 = QLabel(self)
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
        self.images.append(cv.imread(fname, cv.IMREAD_GRAYSCALE))
        self.index += 1
        self.display_image()

    def display_image(self):
        qformat = QImage.Format_Grayscale8

        img = QImage(self.images[self.index], self.images[self.index].shape[1], self.images[self.index].shape[0], qformat)
        #image1 and 2 are for visualisation, for the openCV matrix, look at self.images
        if self.index % 2 == 0:
            self.image1.resize(self.images[self.index].shape[1], self.images[self.index].shape[0])
            self.image1.move(0,0)
            self.image1.setPixmap(QPixmap.fromImage(img))
        else:
            self.image2.resize(self.images[self.index].shape[1], self.images[self.index].shape[0])
            self.image2.move(self.images[self.index-1].shape[0]+1, 0)
            self.image2.setPixmap(QPixmap.fromImage(img))

    def merge_images(self):
        """
        this function merge two images into one, and affect colors to each image (instead of binary)
        for visualisation purpose
        """
        raise NotImplementedError('this function is not implemented')
    
    @pyqtSlot()
    def process_test(self):
        """
        create all the segments possible for the image, then get the parrallels segments
        test if each pixel is contained in one of the segments, only once
        """
        height, width = self.images[0].shape
        seg = functions.get_segment(0, 0, height, height)
        functions.print_segment(seg, height)
        segs = functions.scan_parrallel(seg, height)
        print(functions.test_segments(segs, height, True))
