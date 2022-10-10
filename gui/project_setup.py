"""
GUI welcome widget

@author: Paul Bohn
@contributor: Paul Bohn
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5 import Qt


class Project_Setup(QWidget):
    """
    Tab Welcome Screen
    """
    def __init__(self):
        super().__init__()

        # Caption
        self.title = QLabel('Load Profile Creator')
        self.title.setStyleSheet('font-weight: bold')
        description = 'The Load Profile Creator (LPC) is used to create electric load profiles in a minute-by-minute ' \
                      'resolution based on a data based. The LPC is part of the project Energy-Self-Sufficiency for ' \
                      'Health facilities in Ghana (EnerSHelF) funded by the German Federal Ministry of Education and ' \
                      'Research. \n\n' \
                      'Created by Paul Bohn (University of Applied Science Cologne)'
        self.description = QLabel(description)
        self.description.setWordWrap(True)
        self.th = QLabel()
        th_pixmap = QPixmap('gui/images/th-koeln.png')
        self.th.setPixmap(th_pixmap.scaled(102, 55))

        # Set up Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.title, 0, 0, 1, 2)
        self.layout.addWidget(self.description, 1, 0)
        self.layout.addWidget(self.th, 2, 0)
        self.setLayout(self.layout)
