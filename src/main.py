"""
SpaRe
Projet de TER Taleb Sofiane et Doisneau Gabriel : Spacial Recognition
"""
import sys

from application import App
from PyQt5.QtWidgets import QApplication
import functions
if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #ex = App()
    #sys.exit(app.exec_())
    passed_all = functions.test_all_segments(50)
    print("worked with all segment :", passed_all)