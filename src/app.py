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

    image = None
    image_canvas = None

    hist_obj = None

    # adapting for two images
    images = dict()
    images_canvas = dict()

    position = {
        'TOP': 100,
        'LEFT': 100
    }

    size = {
        'WIDTH': 640,
        'HEIGHT': 400,
    }

    TITLE = 'SpaRe'

    IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'misc')

    def __init__(self):
        super().__init__()        

        self.load_image('black_50_50.png')
        self.load_image('left.png')
        self.load_image('right.png')
        
        self.init_ui()

        ##TODO : merge the two images into one, using a RGB image with A in R and B in G, so we can differentiate them and see if they overlap
        
        # Display all images (2 for now)
        for (fname, image) in self.images_canvas.items():
            image.plot(self.images[fname])
            image.draw()

    def init_ui(self):
        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.position['LEFT'], self.position['TOP'], self.size['WIDTH'], self.size['HEIGHT'])

        # self.btn_add_image = QPushButton('Ajouter une image', self)
        # self.btn_add_image.setToolTip('cliquer pour ajouter une premiere image')
        # self.btn_add_image.move(500, 0)
        # self.btn_add_image.resize(140, 100)
        # self.btn_add_image.clicked.connect(self.load_clicked)

        self.btn_process = QPushButton('Process', self)
        self.btn_process.setToolTip('computation of the histogram.')
        self.btn_process.move(500,250)
        self.btn_process.resize(140, 100)
        self.btn_process.clicked.connect(self.compute_hist)

        self.radio_segment = QRadioButton("segment",self)
        self.radio_segment.setChecked(True)
        self.radio_segment.move(30, 350)

        self.radio_scan_lin = QRadioButton("parralleles", self)
        self.radio_scan_lin.move(200, 350)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(360)
        self.slider.setSingleStep(1)
        self.slider.move(30, 300)
        self.slider.resize(300, 20)

        self.slider.valueChanged.connect(self.draw_bresenham)
        
        self.label_angle = QLabel("0 °",self)
        self.label_angle.move(150, 320)

        self.show()

    def load_image(self, fname):
        self.images[fname] = Image(cv.imread(os.path.join(self.IMAGES_DIR, fname), cv.IMREAD_COLOR))
        self.images_canvas[fname] = ImageCanvas(self, width = 1, height = 1)
        self.images_canvas[fname].move(0 + 256 * list(self.images_canvas.keys()).index(fname), 0)


    @pyqtSlot()
    def compute_hist(self):
        self.hist_obj = Histogram(self.images["left.png"], self.images["right.png"])
        self.hist_obj.compute(relations.angle)
        values = self.hist_obj.get_values()
        self.hist = HistogramCanvas(values, self)
        self.hist.move(0, 400)
        
    def merge_images(self, img_a, img_b):
        height = max(img_a.height, img_b.height)
        width = max(img_a.width, img_b.width)

        self.image = np.zeros((height, width, 3), np.uint8)

        self.image[:][0] = img_a[:][0]
        self.image[:][1] = img_b[:][0]
    
    @pyqtSlot()
    def draw_bresenham(self):
        self.images["black_50_50.png"].reset()
        degree = self.slider.value()
       
        self.label_angle.setText('{} °'.format(degree))
      
         #TODO : add a menu function and dissociate functions
        if self.radio_scan_lin.isChecked():
            parallels = self.images["black_50_50.png"].parallels(degree)
            for segment in parallels:
                self.images["black_50_50.png"].draw(segment)
        else:
            segment = self.images["black_50_50.png"].ray(degree)
            self.images["black_50_50.png"].draw(segment)
        
        self.images_canvas["black_50_50.png"].plot(self.images["black_50_50.png"])
        self.images_canvas["black_50_50.png"].draw()
