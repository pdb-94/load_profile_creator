import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
import datetime as dt


class Room(QWidget):
    def __init__(self):
        super().__init__()

        # Labels
        self.room = QLabel('Room Type')
        self.name = QLabel('Name')
        self.department = QLabel('Department')
        self.time = QLabel('Time Data')
        self.start_time = QLabel('Opening time')
        self.end_time = QLabel('Closing time')
        overview = ('Overview \n(Shows all rooms in\ncurrently selected\ndepartment.)')
        self.overview = QLabel(overview)
        self.overview.setWordWrap(True)
        self.standard = QLabel('Standard rooms')
        self.standard.hide()

        # LineEdits
        self.name_edit = QLineEdit()

        # Combobox
        self.department_combo = QComboBox()
        rooms = ['Individual', 'Standard']
        self.room_type = QComboBox()
        self.room_type.addItems(rooms)
        self.room_type.currentIndexChanged.connect(self.change_layout)
        self.standard_combo = QComboBox()
        standard_rooms = ['Consulting Room', 'Hallway', 'Kitchen', 'Office', 'Ward', 'Washroom']
        self.standard_combo.addItems(standard_rooms)
        self.standard_combo.hide()

        # Date Edit
        self.start_time_edit = QTimeEdit(dt.time(hour=0, minute=0))
        self.end_time_edit = QTimeEdit(dt.time(hour=23, minute=59))

        # ListWidget
        self.viewer = QListWidget()

        # Widget containers
        self.individual_widget = [self.start_time, self.time, self.end_time, self.start_time_edit, self.end_time_edit]
        self.standard_widget = [self.standard, self.standard_combo]

        # Set up Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.room, 0, 0)
        self.layout.addWidget(self.room_type, 0, 1)
        self.layout.addWidget(self.name, 1, 0)
        self.layout.addWidget(self.name_edit, 1, 1)
        self.layout.addWidget(self.department, 2, 0)
        self.layout.addWidget(self.department_combo, 2, 1)
        self.layout.addWidget(self.time, 3, 0)
        self.layout.addWidget(self.standard, 3, 0)
        self.layout.addWidget(self.standard_combo, 3, 1)
        self.layout.addWidget(self.start_time, 4, 0)
        self.layout.addWidget(self.start_time_edit, 4, 1)
        self.layout.addWidget(self.end_time, 5, 0)
        self.layout.addWidget(self.end_time_edit, 5, 1)
        self.layout.addWidget(self.overview, 6, 0)
        self.layout.addWidget(self.viewer, 6, 1)
        self.setLayout(self.layout)

    def change_layout(self):
        """
        Change tab layout based on selection in self.room_type
        :return:
        """
        if self.room_type.currentIndex() == 0:
            for s_widget in self.standard_widget:
                s_widget.hide()
            for i_widget in self.individual_widget:
                i_widget.show()
        elif self.room_type.currentIndex() == 1:
            for i_widget in self.individual_widget:
                i_widget.hide()
            for s_widget in self.standard_widget:
                s_widget.show()
