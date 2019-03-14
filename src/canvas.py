from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.ticker as ticker

import numpy as np

import random, matplotlib.pyplot as plt


class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
 
 
    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')

class ImageCanvas(FigureCanvas):

    def __init__(self, parent = None, width = 5, height = 4, dpi=100):
        fig = Figure(figsize = (width, height), dpi = dpi, frameon = False)
        fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
        FigureCanvas.__init__(self, fig)
        
        self.setParent(parent)

        self.axes = fig.add_subplot(111)
        
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
    def plot(self, image):
        self.axes.axis('off')
        self.axes.imshow(image.image)
        self.show()


class HistogramCanvas(FigureCanvas):
    '''
    This class is used to plt the histogram of the two objects in the main module.
    the values are computed in one of the descriptors.
    #TODO : add the possibility to plot multiple relations in one histogram (changing line type and / or color)
    '''
    def __init__(self, parent = None, is_polar = True, width = 8, height = 5, dpi = 100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.is_polar = is_polar
        self.setParent(parent)
        if self.is_polar:
            self.axes = self.fig.add_subplot(111, projection='polar')
        else :
            self.axes = self.fig.add_subplot(111)
 
        self.axes.grid(True)
        #TODO : Add the names of the objects (fname - extention ?)
        self.axes.set_title("Spatial relations between A and B", va='bottom')
                
        FigureCanvas.updateGeometry(self)

    def plot(self, histogram):
        self.axes.clear()

        if self.is_polar:
            self.axes.set_rlim(0,500)
            theta = [float(k)/ 180 * np.pi for k in histogram.values.keys()]
            #Sorry for that but it works
            if len(theta) > 16:
                i = 0
                theta_major_name = []
                for k in histogram.values.keys():
                    if i % 3 == 0:
                        theta_major_name.append(float(k)/ 180 * np.pi)
                    i+=1
                self.axes.xaxis.set_major_locator(ticker.FixedLocator(theta_major_name))
            else :
                self.axes.xaxis.set_major_locator(ticker.LinearLocator(len(theta)))

            self.axes.xaxis.set_minor_locator(ticker.LinearLocator(len(theta)))
            self.axes.grid(b = True, which='major', linestyle='-')
            self.axes.grid(b = True, which='minor', linestyle='--')
            self.axes.plot(theta, list(histogram.values.values()))
        else:
            self.axes.plot(list(histogram.values.keys()), list(histogram.values.values()))
        self.draw()
    
    def lin_or_polar(self, new_value : bool):
        self.is_polar = new_value
        self.fig.clear()
        if self.is_polar:
            self.axes = self.fig.add_subplot(111, projection='polar')
        else :
            self.axes = self.fig.add_subplot(111)
 
        FigureCanvas.updateGeometry(self)
