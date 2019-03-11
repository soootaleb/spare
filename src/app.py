from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from tests.main import *
from models.image import Image
from models.histogram import Histogram
import relations
from canvas import *

import math, functions, os, sys, cv2 as cv, numpy as np, random

class App(QMainWindow):

    TITLE = 'SpaRe'
    MARGIN_LEFT = 30

    images = dict()
    images_canvas = dict()

    histograms = dict()
    histograms_canvas = dict()

    size = { 'WIDTH': 640, 'HEIGHT': 400 }
    position = { 'TOP': 100, 'LEFT': 100 }


    def __init__(self):
        super().__init__()        

        self.load_image('black_50_50.png')
        self.load_image('left.png')
        self.load_image('right.png')
        
        self.load_hist('left.png', 'right.png')
        
        self.init_ui()

        # TODO : merge the two images into one, using a RGB image with A in R and B in G, so we can differentiate them and see if they overlap
        
        for (fname, image) in self.images_canvas.items():
            image.plot(self.images[fname])

    def init_ui(self):
        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.position['LEFT'], self.position['TOP'], self.size['WIDTH'], self.size['HEIGHT'])

        self.radio_segment = QRadioButton("segment",self)
        self.radio_segment.setChecked(True)
        self.radio_segment.move(self.MARGIN_LEFT, 140)

        self.radio_scan_lin = QRadioButton("parralleles", self)
        self.radio_scan_lin.move(200, 140)

        self.slider_cardinal = QSlider(Qt.Horizontal, self)
        self.slider_cardinal.setMinimum(1)
        self.slider_cardinal.setMaximum(16)
        self.slider_cardinal.setSingleStep(1)
        self.slider_cardinal.move(self.MARGIN_LEFT, 180)
        self.slider_cardinal.resize(300, 20)

        self.slider_angle = QSlider(Qt.Horizontal, self)
        self.slider_angle.setMinimum(0)
        self.slider_angle.setMaximum(360)
        self.slider_angle.setSingleStep(1)
        self.slider_angle.move(self.MARGIN_LEFT, 120)
        self.slider_angle.resize(300, 20)

        self.slider_angle.valueChanged.connect(self.slider_angle_changed)
        self.slider_cardinal.valueChanged.connect(self.slider_cardinal_changed)
        
        self.label_angle = QLabel("0 °", self)
        self.label_angle.move(350, 120)
        
        self.label_cardinal = QLabel("1 angle", self)
        self.label_cardinal.move(350, 180)

        self.show()

    def load_image(self, fname):
        self.images[fname] = Image(fname).resize(1/8)
        self.images_canvas[fname] = ImageCanvas(self, width = 1, height = 1)
        self.images_canvas[fname].move(self.MARGIN_LEFT + 150 * list(self.images_canvas.keys()).index(fname), 0)

    def load_hist(self, fname_a, fname_b):
        hist = fname_a + fname_b

        self.histograms[hist] = Histogram(self.images["left.png"], self.images["right.png"])
        
        self.histograms_canvas[hist] = HistogramCanvas(self)
        self.histograms_canvas[hist].move(self.MARGIN_LEFT, 220)
        
    # def merge_images(self, img_a, img_b):
    #     height = max(img_a.height, img_b.height)
    #     width = max(img_a.width, img_b.width)

    #     self.image = np.zeros((height, width, 3), np.uint8)

    #     self.image[:][0] = img_a[:][0]
    #     self.image[:][1] = img_b[:][0]


    @pyqtSlot()
    def slider_cardinal_changed(self):
        self.label_cardinal.setText('{} angle'.format(self.slider_cardinal.value()))

        cardinal = self.slider_cardinal.value()

        for (hname, canvas) in self.histograms_canvas.items():
            self.histograms[hname] \
                .set_cardinal(cardinal) \
                .compute(relations.angle)

            self.histograms_canvas[hname].plot(self.histograms[hname])
        
    
    @pyqtSlot()
    def slider_angle_changed(self):
        self.images["black_50_50.png"].reset()
        
        degree = self.slider_angle.value()
       
        self.label_angle.setText('{} °'.format(degree))
      
        if self.radio_scan_lin.isChecked():
            parallels = self.images["black_50_50.png"].parallels(degree)
            for segment in parallels:
                self.images["black_50_50.png"].draw(segment)
        else:
            segment = self.images["black_50_50.png"].ray(degree)
            self.images["black_50_50.png"].draw(segment)
        
        self.images_canvas["black_50_50.png"].plot(self.images["black_50_50.png"])
        self.images_canvas["black_50_50.png"].draw()
