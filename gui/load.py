"""
GUI module to create load

@author: Paul Bohn
@contributor: Paul Bohn
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *


class Consumer(QWidget):
    """
    Tab to create Load object
    """
    def __init__(self):
        super().__init__()

        self.consumer_list = []
        overview = 'Overview \n(Shows all consumers based \n' \
                   'on currently selected room.)'

        # Labels
        self.name = QLabel('Name')
        self.department = QLabel('Department')
        self.room = QLabel('Room')
        self.type = QLabel('Load type')
        self.overview = QLabel(overview)
        self.overview.setWordWrap(True)

        # LineEdits
        self.name_edit = QLineEdit()

        # ComboBox
        self.department_combo = QComboBox()
        self.room_combo = QComboBox()
        self.type_combo = QComboBox()
        load_type = ['Constant', 'Sequential', 'Cycle']
        self.type_combo.addItems(load_type)

        # ListWidget
        self.viewer = QListWidget()

        # Set up Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.name, 0, 0)
        self.layout.addWidget(self.name_edit, 0, 1)
        self.layout.addWidget(self.department, 1, 0)
        self.layout.addWidget(self.department_combo, 1, 1)
        self.layout.addWidget(self.room, 2, 0)
        self.layout.addWidget(self.room_combo, 2, 1)
        self.layout.addWidget(self.type, 3, 0)
        self.layout.addWidget(self.type_combo, 3, 1)
        self.layout.addWidget(self.overview, 4, 0)
        self.layout.addWidget(self.viewer, 4, 1)
        self.setLayout(self.layout)
