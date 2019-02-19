
# We need to change the used backend to not rely on the system one
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets as widgets
import matplotlib.pyplot as plt


if __name__ == "__main__":

    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.show()

    app = widgets.QApplication([])
    label = widgets.QLabel('Hello World')
    label.show()
    app.exec()