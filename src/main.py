"""
SpaRe
Projet de TER Taleb Sofiane et Doisneau Gabriel : Spacial Recognition
"""

import matplotlib, sys, functions

# We need to change the used backend to not rely on the system one
matplotlib.use('Qt5Agg')

from app import App
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
