from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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
    def __init__(self, parent = None, width =4, height = 4, dpi = 100, cardinal = 16):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.r = 2 * np.linspace(1, cardinal)#TODO : Add the real values for the histogram

        self.theta = 2* np.pi * self.r #TODO : Add the real values for the histogram
        
        self.axes = fig.add_subplot(111, projection='polar')
        self.axes.set_rmax(2)
        self.axes.set_rlabel_position(-22.5)  # get radial labels away from plotted line
        self.axes.grid(True)
        self.axes.set_title("spatial relations between A and B", va='bottom')

        self.plot()
    
    def plot(self):
        self.axes.bar(self.theta, self.r)
        self.show()