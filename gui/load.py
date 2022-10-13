"""
GUI module to create load

@author: Paul Bohn
@contributor: Paul Bohn
"""

from PyQt5.Qt import *
import gui.gui_function as gui_func


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
        self.power = QLabel('Power [W]')
        self.standby = QLabel('Standby [W]')
        self.overview = QLabel(overview)
        self.overview.setWordWrap(True)

        # LineEdits
        self.name_edit = QLineEdit()
        self.power_edit = QLineEdit()
        self.standby_edit = QLineEdit()

        # ComboBox
        self.department_combo = QComboBox()
        self.room_combo = QComboBox()
        self.type_combo = QComboBox()
        load_type = ['Constant', 'Sequential', 'Cycle']
        self.type_combo.addItems(load_type)
        self.type_combo.currentIndexChanged.connect(self.load_type_changed)

        # ListWidget
        self.viewer = QListWidget()

        # Additional widgets
        self.cycle_length = QLabel('Cycle length')
        self.cycle_length_edit = QLineEdit()
        self.interval_open = QLabel('Interval (open)')
        self.interval_open_edit = QLineEdit()
        self.interval_closed = QLabel('Interval (closed)')
        self.interval_closed_edit = QLineEdit()
        self.cycle = QLabel('Load cycle csv-file')
        self.cycle_edit = QLineEdit()
        self.profile = QLabel('Profile csv-file')
        self.profile_edit = QLineEdit()

        self.sequential_widgets = [self.cycle_length, self.cycle_length_edit,
                                   self.interval_open, self.interval_open_edit,
                                   self.interval_closed, self.interval_closed_edit]

        self.cycle_widgets = [self.cycle_length, self.cycle_length_edit,
                              self.cycle, self.cycle_edit,
                              self.profile, self.profile_edit]

        gui_func.show_widget(widget=self.sequential_widgets, show=False)
        gui_func.show_widget(widget=self.cycle_widgets, show=False)

        # Set up Layout
        self.layout = QGridLayout()
        # Basic widgets
        self.layout.addWidget(self.name, 0, 0)
        self.layout.addWidget(self.name_edit, 0, 1)
        self.layout.addWidget(self.department, 1, 0)
        self.layout.addWidget(self.department_combo, 1, 1)
        self.layout.addWidget(self.room, 2, 0)
        self.layout.addWidget(self.room_combo, 2, 1)
        self.layout.addWidget(self.type, 3, 0)
        self.layout.addWidget(self.type_combo, 3, 1)
        self.layout.addWidget(self.power, 4, 0)
        self.layout.addWidget(self.power_edit, 4, 1)
        self.layout.addWidget(self.standby, 5, 0)
        self.layout.addWidget(self.standby_edit, 5, 1)
        self.layout.addWidget(self.overview, 9, 0)
        self.layout.addWidget(self.viewer, 9, 1)
        # Additional widgets
        self.layout.addWidget(self.cycle_length, 6, 0)
        self.layout.addWidget(self.cycle_length_edit, 6, 1)
        # Sequential widgets
        self.layout.addWidget(self.interval_open, 7, 0)
        self.layout.addWidget(self.interval_open_edit, 7, 1)
        self.layout.addWidget(self.interval_closed, 8, 0)
        self.layout.addWidget(self.interval_closed_edit, 8, 1)
        # Cycle widgets
        self.layout.addWidget(self.cycle, 7, 0)
        self.layout.addWidget(self.cycle_edit, 7, 1)
        self.layout.addWidget(self.profile, 8, 0)
        self.layout.addWidget(self.profile_edit, 8, 1)

        self.setLayout(self.layout)

    def load_type_changed(self):
        """
        Show/hide widgets based on selected load type
        :return: None
        """
        index = self.type_combo.currentIndex()
        if index == 0:
            # Constant
            for widget in self.sequential_widgets:
                widget.hide()
            for widget in self.cycle_widgets:
                widget.hide()
        elif index == 1:
            for widget in self.cycle_widgets:
                widget.hide()
            for widget in self.sequential_widgets:
                widget.show()
        elif index == 2:
            for widget in self.sequential_widgets:
                widget.hide()
            for widget in self.cycle_widgets:
                widget.show()
