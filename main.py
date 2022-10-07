import sys
from PyQt5.QtWidgets import *
from gui.tab_widget import TabWidget


app = QApplication(sys.argv)
lpc = TabWidget()
sys.exit(app.exec())
