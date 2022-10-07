import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *


class Hospital(QWidget):
    def __init__(self):
        super().__init__()

        self.name = QLabel('Project Name')
        self.time = QLabel('Time Data')
        self.start_time = QLabel('Start time')
        self.end_time = QLabel('End time')
        self.time_step = QLabel('Resolution')
        self.overview = QLabel('Overview')

        # LineEdits
        self.name_edit = QLineEdit()

        # Date Edit
        self.start_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_time_edit.setCalendarPopup(True)
        self.end_time_edit = QDateTimeEdit(QDateTime.currentDateTime().addDays(1))
        self.end_time_edit.setCalendarPopup(True)
        self.time_step_edit = QTimeEdit(QTime(0, 1))

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
        self.layout.addWidget(self.time_step, 4, 0)
        self.layout.addWidget(self.time_step_edit, 4, 1)
        self.layout.addWidget(self.overview, 5, 0)
        self.layout.addWidget(self.viewer, 5, 1)
        self.setLayout(self.layout)
