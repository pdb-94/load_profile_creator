import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
import datetime as dt


class Department(QWidget):
    def __init__(self):
        super().__init__()

        # Labels
        self.name = QLabel('Name')
        self.time = QLabel('Time Data')
        self.start_time = QLabel('Opening time')
        self.end_time = QLabel('Closing time')
        self.overview = QLabel('Overview')

        # LineEdits
        self.name_edit = QLineEdit()

        # Date Edit
        self.start_time_edit = QTimeEdit(dt.time(hour=0, minute=0))
        self.end_time_edit = QTimeEdit(dt.time(hour=23, minute=59))

        # ListWidget
        self.viewer = QListWidget()

        # Set up Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.name, 0, 0)
        self.layout.addWidget(self.name_edit, 0, 1)
        self.layout.addWidget(self.time, 1, 0)
        self.layout.addWidget(self.start_time, 2, 0)
        self.layout.addWidget(self.start_time_edit, 2, 1)
        self.layout.addWidget(self.end_time, 3, 0)
        self.layout.addWidget(self.end_time_edit, 3, 1)
        self.layout.addWidget(self.overview, 4, 0)
        self.layout.addWidget(self.viewer, 4, 1)
        self.setLayout(self.layout)

