"""
SpaRe
Projet de TER Taleb Sofiane et Doisneau Gabriel : Spacial Recognition
"""
import matplotlib
import cv2 as cv
import random, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import(QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy,
    QMessageBox, QWidget, QPushButton, QFileDialog, QLabel)
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
        self.spares = []
        self.index = -1
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)
 
        self.button = QPushButton('Ajouter une image', self)
        self.button.setToolTip('cliquer pour ajouter la premiere image')
        self.button.move(500, 0)
        self.button.resize(140, 100)
        self.button.clicked.connect(self.loadClicked)
        self.label = QLabel(self)
        self.show()

    @pyqtSlot()
    def loadClicked(self):
        base_path=".\misc"
        #fname, filter = QFileDialog.getOpenFileName(self, 'Open File', base_path, "Image Files(*.jpg, *.png)")
        fname = "./misc/black_50_50.png"
        if fname:
            self.loadImage(fname)
        else:
            print('invalid image')
    
    def loadImage(self,fname):
        self.image = cv.imread(fname, cv.IMREAD_COLOR)
        self.displayImage()
        
    def displayImage(self):
        qformat = QImage.Format_Indexed8
        print(self.image.shape)
        print(self.image.strides)
        if len(self.image.shape) == 3:
            if(self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
            img = QImage(self.image, self.image.shape[1], self.image.shape[0], qformat)
            img = img.rgbSwapped()
            print(self.image.shape[1], self.image.shape[0], self.image.strides[0])
            self.spares.append(img)
            self.index += 1
            self.label.setPixmap(QPixmap.fromImage(img))
            #self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)



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

    def get_segments(self, x1, y1, x2, y2):
        """
        tracé de segment d'apres l'algorithme de bresenham
        (x1 y1) : le point de départ en haut a gauche, (x2 y2) point d'arrivé en bas a droite.
        retourne une liste contenant les double (x, y) de chacun des points.
        """
        segment = [] #Contient tout les pixels du segment.
        print("TODO")
        delta_x = x2 - x1
        delta_y = y2 - y1
        y = y1 #rangée de départ
        error = 0.0
        if(delta_x != 0):
            err_x = delta_y / delta_x
        else:
           err_x = 0

        err_y = -1

        for x in range(x1, x2):
            segment.append([x, y])
            error += err_x
            if (error >= 0.5):
                y += 1
                error += err_y
        return segment

    def histogram(self, cardinal=16):
        """
        creation de l'histograme selon le nombres de directions données en entrée
        """
        #TODO    
        print("TODO")
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())