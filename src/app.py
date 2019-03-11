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
    IMAGE_RESIZE_FACTOR = 1/8
    CARDINAL_MAXIMUM = 32

    images = dict()
    images_canvas = dict()

    histograms = dict()
    histograms_canvas = dict()

    size = { 'WIDTH': 640, 'HEIGHT': 400 }
    position = { 'TOP': 100, 'LEFT': 100 }


    def __init__(self):
        super().__init__()        

        self.load_image('left.png')
        self.load_image('right.png')

        self.images['merged_images'] = self.images['left.png'].merge(self.images['right.png'])
        self.images_canvas['merged_images'] = ImageCanvas(self, width = 1, height = 1)
        self.images_canvas['merged_images'].move(self.MARGIN_LEFT + 150 * list(self.images_canvas.keys()).index('merged_images'), 10)

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
        self.radio_segment.move(self.MARGIN_LEFT + 50, 140)

        self.radio_scan_lin = QRadioButton("parralleles", self)
        self.radio_scan_lin.move(250, 140)

        self.slider_cardinal = QSlider(Qt.Horizontal, self)
        self.slider_cardinal.setMinimum(1)
        self.slider_cardinal.setMaximum(self.CARDINAL_MAXIMUM)
        self.slider_cardinal.setSingleStep(1)
        self.slider_cardinal.move(self.MARGIN_LEFT, 180)
        self.slider_cardinal.resize(300, 20)

        self.slider_angle = QSlider(Qt.Horizontal, self)
        self.slider_angle.setMinimum(0)
        self.slider_angle.setMaximum(360)
        self.slider_angle.setSingleStep(1)
        self.slider_angle.move(self.MARGIN_LEFT, 120)
        self.slider_angle.resize(300, 20)

        self.slider_rotate = QSlider(Qt.Horizontal, self)
        self.slider_rotate.setMinimum(-90)
        self.slider_rotate.setMaximum(90)
        self.slider_rotate.setSingleStep(10)
        self.slider_rotate.move(self.MARGIN_LEFT + 150 * len(self.images_canvas.keys()), 50)
        self.slider_rotate.resize(200, 20)

        self.slider_angle.valueChanged.connect(self.slider_angle_changed)
        self.slider_rotate.valueChanged.connect(self.slider_rotate_changed)
        self.slider_cardinal.valueChanged.connect(self.slider_cardinal_changed)
        
        self.label_angle = QLabel("0 ° rays", self)
        self.label_angle.move(350, 120)
        
        self.label_cardinal = QLabel("1 angle", self)
        self.label_cardinal.move(350, 180)
        
        self.label_rotate = QLabel("0° rotation", self)
        self.label_rotate.move(self.MARGIN_LEFT + 150 * len(self.images_canvas.keys()) + 100, 20)

        self.show()

    def load_image(self, fname):
        self.images[fname] = Image(fname).resize(self.IMAGE_RESIZE_FACTOR)
        self.images_canvas[fname] = ImageCanvas(self, width = 1, height = 1)
        self.images_canvas[fname].move(self.MARGIN_LEFT + 150 * list(self.images_canvas.keys()).index(fname), 10)

    def load_hist(self, fname_a, fname_b):
        hist = fname_a + fname_b
        self.histograms[hist] = Histogram(self.images["left.png"], self.images["right.png"])        
        self.histograms_canvas[hist] = HistogramCanvas(self)
        self.histograms_canvas[hist].move(self.MARGIN_LEFT, 220)

    @pyqtSlot()
    def slider_rotate_changed(self):
        self.images['right.png'] \
            .reset() \
            .resize(self.IMAGE_RESIZE_FACTOR)

        self.images['merged_images'] \
            .reset() \
            .resize(self.IMAGE_RESIZE_FACTOR)

        rotation = self.slider_rotate.value()
        self.label_rotate.setText('{}° rotation'.format(rotation))
        self.images['merged_images'] = self.images['left.png'].merge(self.images['right.png'].rotate(rotation))
        self.slider_angle_changed()

    @pyqtSlot()
    def slider_cardinal_changed(self):
        cardinal = self.slider_cardinal.value()
        self.label_cardinal.setText('{} angle'.format(cardinal))

        # This part draws the directions on the images
        # The directions are only the ones with positive values on the histogram
        for (hname, canvas) in self.histograms_canvas.items():

            self.histograms[hname] \
                .set_cardinal(cardinal) \
                .compute(relations.angle)

            self.histograms_canvas[hname].plot(self.histograms[hname])
        

    @pyqtSlot()
    def slider_angle_changed(self):
        self.images['merged_images'].reset()
        
        degree = self.slider_angle.value()
       
        self.label_angle.setText('{} °'.format(degree))
      
        if self.radio_scan_lin.isChecked():
            parallels = self.images['merged_images'].parallels(degree)
            for segment in parallels:
                self.images['merged_images'].draw(segment)
        else:
            segment = self.images['merged_images'].ray(degree)
            self.images['merged_images'].draw(segment)
        
        self.images_canvas['merged_images'].plot(self.images['merged_images'])
        self.images_canvas['merged_images'].draw()
