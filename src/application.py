from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from canvas import *

import math, functions, os, sys, cv2 as cv, numpy as np

class App(QMainWindow):

    image = None
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
            self.image_canvas = ImageCanvas(self, width = 2, height = 2)
            self.image_canvas.move(0, 0)
        else:
            raise FileNotFoundError('The image ' + image + ' does not exist')
        

    @pyqtSlot()
    def process_test(self):
        """
        Create all the segments giving and test scan parralels
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
