from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from canvas import *

import math, functions, os, sys, cv2 as cv, numpy as np, random

class App(QMainWindow):

    image = None
    image_base = None
    image_canvas = None

    index = -1 # For multiple images
    images = [] # For multiple images

    position = {
        'TOP': 100,
        'LEFT': 100
    }

    size = {
        'WIDTH': 640,
        'HEIGHT': 400,
    }

    TITLE = 'SpaRe'

    def __init__(self):
        super().__init__()        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.position['LEFT'], self.position['TOP'], self.size['WIDTH'], self.size['HEIGHT'])

        self.btn_add_image = QPushButton('Ajouter une image', self)
        self.btn_add_image.setToolTip('cliquer pour ajouter une premiere image')
        self.btn_add_image.move(500, 0)
        self.btn_add_image.resize(140, 100)
        self.btn_add_image.clicked.connect(self.load_clicked)

        self.radio_segment = QRadioButton("segment",self)
        self.radio_segment.setChecked(True)
        self.radio_segment.move(0, 350)

        self.radio_scan_lin = QRadioButton("parralleles", self)
        self.radio_scan_lin.move(200, 350)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(360)
        self.slider.setSingleStep(1)
        self.slider.move(0, 300)
        self.slider.resize(300, 20)

        self.slider.valueChanged.connect(self.draw_bresenham)
        
        self.label_angle = QLabel("0 °",self)
        self.label_angle.move(0, 320)
        
        self.show()

    '''
    Loads & display image "black_50_50.png"
    '''
    @pyqtSlot()
    def load_clicked(self):
        '''
        Reads and image with OpenCV & displays it with self.display_image()
        '''
        base_path= os.path.dirname(os.path.dirname(__file__))
        fname = 'black_50_50.png'
        if fname:
            self.image = cv.imread(os.path.join(base_path, 'misc', fname), cv.IMREAD_COLOR)
            self.image_base = cv.imread(os.path.join(base_path, 'misc', fname), cv.IMREAD_COLOR)
            self.image_canvas = ImageCanvas(self, width = 3, height = 3)
            self.image_canvas.move(0, 0)
        else:
            raise FileNotFoundError('The image ' + image + ' does not exist')
        
    @pyqtSlot()
    def draw_bresenham(self):
        if self.image_base is None:
            self.load_clicked()

        self.image = self.image_base.copy()
        
        degree = self.slider.value()

        self.label_angle.setText('{} °'.format(degree))

        width = self.image.shape[1]
        height = self.image.shape[0]
        
        max_lenght = max(height, width)

        segment = functions.bresenham_angle(degree, max_lenght)
       
        #TODO : add a menu function and dissociate functions

        if self.radio_scan_lin.isChecked():
            segments = functions.scan_parrallel(segment, width)
            for se in segments:
                
                color = [random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]

                for (x, y) in se:
                    color = [max(0, color[0]-2), max(0, color[1]-2), max(0, color[2]-2)]
                    if x < width and y < height:
                        self.image[x, y] = color
        else:
            color = [255, 0, 0]
            for (x, y) in segment:
                color[0] = color[0] -3
                if x < width and y < height:
                    self.image[x, y] = color

        self.image_canvas.plot()
        self.image_canvas.draw()
