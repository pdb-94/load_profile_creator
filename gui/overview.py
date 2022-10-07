import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from PyQt5 import QtCore


class Overview(QWidget):
    def __init__(self):
        super().__init__()

        # Labels
        self.overview = QLabel('Overview')

        # ListWidget
        self.viewer = QListWidget()

        # Set up Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.overview, 4, 0)
        self.layout.addWidget(self.viewer, 4, 1)
        self.setLayout(self.layout)
