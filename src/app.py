from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from models.image import Image
from models.histogram import Histogram
from descriptors import *
from serializers import *
import relations
from canvas import *

import math, functions, os, sys, cv2 as cv, numpy as np, random

class App(QMainWindow):

    TITLE = 'SpaRe'
    MARGIN_LEFT = 30
    CARDINAL_MAXIMUM = 32
    VARIANCE_MAXIMUM = 50
    
    IMG_REF_NAME = 'reference.png'
    IMG_REL_NAME = 'relative.png'

    images = dict()
    variance = 20
    images_canvas = dict()
    image_resize_factor = 1/8

    descriptors = dict()
    histograms_canvas = dict()

    size = { 'WIDTH': 800, 'HEIGHT': 600 }
    position = { 'TOP': 100, 'LEFT': 100 }

    def __init__(self):
        super().__init__()        
        self.load_images()
        self.load_descriptors()
        self.init_ui()
        
        for (fname, image) in self.images_canvas.items():
            image.plot(self.images[fname])

    def load_images(self):
        self.images[self.IMG_REF_NAME] = Image(self.IMG_REF_NAME).resize(self.image_resize_factor)
        self.images_canvas[self.IMG_REF_NAME] = ImageCanvas(self, width = 1, height = 1)
        self.images_canvas[self.IMG_REF_NAME].move(self.MARGIN_LEFT + 150 * list(self.images_canvas.keys()).index(self.IMG_REF_NAME), 10)

        self.images[self.IMG_REL_NAME] = Image(self.IMG_REL_NAME).resize(self.image_resize_factor)
        self.images_canvas[self.IMG_REL_NAME] = ImageCanvas(self, width = 1, height = 1)
        self.images_canvas[self.IMG_REL_NAME].move(self.MARGIN_LEFT + 150 * list(self.images_canvas.keys()).index(self.IMG_REL_NAME), 10)

        self.images['merged_images'] = self.images[self.IMG_REF_NAME].merge(self.images[self.IMG_REL_NAME])
        self.images_canvas['merged_images'] = ImageCanvas(self, width = 1, height = 1)
        self.images_canvas['merged_images'].move(self.MARGIN_LEFT + 150 * list(self.images_canvas.keys()).index('merged_images'), 10)

    def load_descriptors(self):
        self.descriptors[OverlappingDescriptor.__name__] = OverlappingDescriptor(self.images[self.IMG_REF_NAME], self.images[self.IMG_REL_NAME], variance= self.variance)
        self.descriptors[AngularPresenceDescriptor.__name__] = AngularPresenceDescriptor(self.images[self.IMG_REF_NAME], self.images[self.IMG_REL_NAME], variance= self.variance)

        self.histograms_canvas = HistogramCanvas(self, height = 3, width = 6)
        self.histograms_canvas.move(self.MARGIN_LEFT, 290)

    def init_ui(self):
        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.position['LEFT'], self.position['TOP'], self.size['WIDTH'], self.size['HEIGHT'])

        #DEBUG MODE
        self.radio_segment = QRadioButton('Segment',self)
        self.radio_segment.setChecked(True)
        self.radio_segment.move(self.MARGIN_LEFT + 50, 140)

        self.radio_scan_lin = QRadioButton('Parralleles', self)
        self.radio_scan_lin.move(250, 140)

        parallels_group = QButtonGroup(self)
        parallels_group.addButton(self.radio_segment)
        parallels_group.addButton(self.radio_scan_lin)

        ##HITOGRAM TYPE
        self.check_hist_type = QCheckBox("Polar histogram", self)
        self.check_hist_type.move(self.MARGIN_LEFT + 420, 180)
        self.check_hist_type.setChecked(True)
        self.check_hist_type.resize(150, 20)

        self.check_hist_type.toggled.connect(self.change_hist_type)

        ##CARDINAL
        self.slider_cardinal = QSlider(Qt.Horizontal, self)
        self.slider_cardinal.setMinimum(1)
        self.slider_cardinal.setMaximum(self.CARDINAL_MAXIMUM)
        self.slider_cardinal.setValue(16)
        self.slider_cardinal.setSingleStep(1)
        self.slider_cardinal.move(self.MARGIN_LEFT, 180)
        self.slider_cardinal.resize(300, 20)

        self.label_cardinal = QLabel("16 angle", self)
        self.label_cardinal.move(350, 180)

        self.slider_cardinal.valueChanged.connect(self.slider_cardinal_changed)


        ##VARIANCE 
        self.slider_variance = QSlider(Qt.Horizontal, self)
        self.slider_variance.setMinimum(1)
        self.slider_variance.setMaximum(self.VARIANCE_MAXIMUM)
        self.slider_variance.setValue(self.variance)
        self.slider_variance.setSingleStep(1)
        self.slider_variance.move(self.MARGIN_LEFT, 220)
        self.slider_variance.resize(300, 20)
    
        self.label_variance = QLabel("Variance :{}".format(self.variance), self)
        self.label_variance.move(self.MARGIN_LEFT + 300, 220)

        self.slider_variance.valueChanged.connect(self.slider_variance_changed)        

        ##ANGLE NUMBER : cardinal of the histogram (impacts performances)
        self.slider_angle = QSlider(Qt.Horizontal, self)
        self.slider_angle.setValue(16)
        self.slider_angle.setMinimum(0)
        self.slider_angle.setMaximum(360)
        self.slider_angle.setSingleStep(1)
        self.slider_angle.move(self.MARGIN_LEFT, 120)
        self.slider_angle.resize(300, 20)
        
        
        self.label_angle = QLabel("0 ° rays", self)
        self.label_angle.move(350, 120)

        self.slider_angle.valueChanged.connect(self.slider_angle_changed)        

        ##RESIZE FACTOR : cardinal of the histogram (greatly impacts performances)
        self.slider_resize_factor = QSlider(Qt.Horizontal, self)
        self.slider_resize_factor.setValue(8)
        self.slider_resize_factor.setMinimum(1)
        self.slider_resize_factor.setMaximum(12)
        self.slider_resize_factor.setSingleStep(1)
        self.slider_resize_factor.move(self.MARGIN_LEFT+500, 120)
        self.slider_resize_factor.resize(100, 20)
        
        
        self.label_resize_factor = QLabel('Resize factor 1/8', self)
        self.label_resize_factor.move(650, 120)
        self.label_resize_factor.resize(150, 20)

        self.slider_resize_factor.valueChanged.connect(self.slider_resize_changed)        


        ##ROTATION : moving the reference image in a circle
        self.slider_rotate = QSlider(Qt.Horizontal, self)
        self.slider_rotate.setMinimum(-180)
        self.slider_rotate.setMaximum(180)
        self.slider_rotate.setSingleStep(10)
        self.slider_rotate.move(self.MARGIN_LEFT + 150 * len(self.images_canvas.keys()), 50)
        self.slider_rotate.resize(200, 20)
        
        self.label_rotate = QLabel("0° rotation", self)
        self.label_rotate.move(self.MARGIN_LEFT + 150 * len(self.images_canvas.keys()) + 100, 20)

        self.slider_rotate.valueChanged.connect(self.slider_rotate_changed)

        ##TEXT INTERPRETATION : A is reference, B is relative
        self.label_interpretation = QLabel(self)
        self.label_interpretation.resize(self.size["WIDTH"], 50)
        self.label_interpretation.move(self.MARGIN_LEFT, 240)


        # Save button
        self.save_button = QPushButton('Save histogram', self)
        self.save_button.clicked.connect(self.save_button_clicked)
        self.save_button.resize(130, 40)
        self.save_button.move(600, 180)

        # Serializer selector
        self.serializer_json = QRadioButton('json', self)
        self.serializer_json.setChecked(True)
        self.serializer_json.move(600, 230)
        self.serializer_csv = QRadioButton('csv', self)
        self.serializer_csv.move(700, 230)

        formats_group = QButtonGroup(self)
        formats_group.addButton(self.serializer_json)
        formats_group.addButton(self.serializer_csv)

        self.show()

    @pyqtSlot()
    def save_button_clicked(self):
        for desc in self.descriptors.values():
            if self.serializer_json.isChecked():
                desc.histogram.save(json_serializer)
            else:
                desc.histogram.save(csv_serializer)

    @pyqtSlot()
    def slider_resize_changed(self):
        
        self.image_resize_factor = 1 / self.slider_resize_factor.value()

        self.label_resize_factor.setText('Resize factor 1/{}'.format(str(self.slider_resize_factor.value())))
        
        self.images[self.IMG_REF_NAME] \
            .reset() \
            .resize(self.image_resize_factor)
        self.images_canvas[self.IMG_REF_NAME].plot(self.images[self.IMG_REF_NAME])
        self.images_canvas[self.IMG_REF_NAME].draw()

        self.slider_rotate_changed()

    @pyqtSlot()
    def slider_rotate_changed(self):
        rotation = self.slider_rotate.value()
        self.images[self.IMG_REL_NAME] \
            .reset() \
            .resize(self.image_resize_factor) \
            .rotate(rotation)
        self.images_canvas[self.IMG_REL_NAME].plot(self.images[self.IMG_REL_NAME])
        self.images_canvas[self.IMG_REL_NAME].draw()

        self.images['merged_images'] \
            .reset() \
            .resize(self.image_resize_factor)

        self.label_rotate.setText('{}° rotation'.format(rotation))
        self.images['merged_images'] = self.images[self.IMG_REF_NAME].merge(self.images[self.IMG_REL_NAME])
        
        self.images_canvas['merged_images'].plot(self.images['merged_images'])
        self.images_canvas['merged_images'].draw()
        self.slider_cardinal_changed()

    @pyqtSlot()
    def slider_cardinal_changed(self):
        self.histograms_canvas.clear()
        cardinal = self.slider_cardinal.value()
        self.label_cardinal.setText('{} angle'.format(cardinal))
        textual_interpretation = self.IMG_REF_NAME[0:self.IMG_REF_NAME.index('.')] + ' is '
        add_and = False
        for (dname, descriptor) in self.descriptors.items():
            descriptor.set_cardinal(cardinal) \
                .compute_histogram() \
                .describe()
            self.histograms_canvas.plot(descriptor.histogram)
            temporary = descriptor.interpret()
            if add_and and temporary != "":
                temporary ="and "+temporary
                add_and = False
            if temporary != "":
                add_and = True

            textual_interpretation += temporary

            #update the histograms values
        #update textual interpretation
        textual_interpretation += self.IMG_REL_NAME[0:self.IMG_REL_NAME.index('.')]
        self.label_interpretation.setText(textual_interpretation)
        self.change_font()

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

    @pyqtSlot()
    def slider_variance_changed(self):
        '''
        change the variance in the interpretation of the descriptors (as we use gaussian density function)
        '''
        value = self.slider_variance.value()
        self.label_variance.setText("Variance :{}".format(value))
        for desc in self.descriptors.values():
            desc.set_variance(value) 
        self.slider_cardinal_changed()
    
    @pyqtSlot()
    def change_hist_type(self):
        '''
            Change the histogram type : polar or linear.
        '''
        is_checked = self.check_hist_type.isChecked()
        
        for (dname, descriptor) in self.descriptors.items():
            self.histograms_canvas.lin_or_polar(is_checked)
            self.histograms_canvas.plot(descriptor.histogram)
    
    @pyqtSlot()    
    def change_font(self):
        
        # Computing accuracy
        accuracy = 0.0
        for (dname, descriptor) in self.descriptors.items():
            accuracy += descriptor.safety()

        if accuracy < 0.6:
            color ="red"
        elif accuracy < 0.8:
            color = "orange"
        else : 
            color = "green"
        self.label_interpretation.setStyleSheet("font-size : 20px; color: {}".format(color))