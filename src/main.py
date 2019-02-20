"""
SpaRe
Projet de TER Taleb Sofiane et Doisneau Gabriel : Spacial Recognition
"""
import matplotlib
import cv2 as cv
import random, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
# We need to change the used backend to not rely on the system one
matplotlib.use('Qt5Agg')

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.title = 'SpaRe'
        self.width = 640
        self.height = 400
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)
 
        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This s an example button')
        button.move(500,0)
        button.resize(140,100)
 
        self.show()
 
 
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
 
 
    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

class Spare():
    """
    reconnaissance de relation spatiale entre les images binaires A et B
    """
    def __init__(self, imgA, imgB):
        A = cv.imread(imgA, cv.IMREAD_GRAYSCALE)
        B = cv.imread(imgB, cv.IMREAD_GRAYSCALE)

    def brensenham():
        """
        tracé de segment d'apres l'algorithme de bresenham
        """
        print("TODO")
        #TODO

    def histogram(cardinal=16):
        """
        creation de l'histograme selon le nombres de directions données en entrée
        """
        #TODO    
        print("todo")
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())