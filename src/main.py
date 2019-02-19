
from PyQt5 import QtWidgets as widgets

if __name__ == "__main__":
    app = widgets.QApplication([])
    label = widgets.QLabel('Hello World')
    label.show()
    app.exec()