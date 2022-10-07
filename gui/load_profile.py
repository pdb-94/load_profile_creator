"""
GUI widget to display load profiles

@author: Paul Bohn
@contributor: Paul Bohn
"""

__version__ = '0.1'
__author__ = 'pdb-94'


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from PyQt5 import QtCore
from gui.plot import *


class Load_profile(QWidget):
    """
    Tab to display load_profiles
    """
    def __init__(self):
        super().__init__()

        # Set Up Labels
        self.level_1 = QLabel('Load profile level')
        self.level_2 = QLabel('Load profile')
        self.level_3 = QLabel('Room')
        self.level_4 = QLabel('Consumer')
        self.level_2.hide()
        self.level_3.hide()
        self.level_4.hide()

        # Container for ComboBoxes
        self.hospital = []
        self.department = []
        self.room = []
        self.consumer = []

        # Set up Combobox
        levels = ['Hospital', 'Department', 'Room', 'Consumer']
        self.level_1_combo = QComboBox()
        self.level_1_combo.addItems(levels)
        self.level_2_combo = QComboBox()
        self.level_2_combo.setEnabled(False)
        self.level_3_combo = QComboBox()
        self.level_4_combo = QComboBox()
        self.level_2_combo.hide()
        self.level_3_combo.hide()
        self.level_4_combo.hide()

        # Set up Plot
        self.plot = Plot()
        self.toolbar = self.toolbar = NavigationToolbar(self.plot, self)

        # Set up Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.level_1, 1, 0)
        self.layout.addWidget(self.level_1_combo, 1, 1)
        self.layout.addWidget(self.level_2, 2, 0)
        self.layout.addWidget(self.level_2_combo, 2, 1)
        self.layout.addWidget(self.level_3, 3, 0)
        self.layout.addWidget(self.level_3_combo, 3, 1)
        self.layout.addWidget(self.level_4, 4, 0)
        self.layout.addWidget(self.level_4_combo, 4, 1)
        self.layout.addWidget(self.toolbar, 5, 0, 1, 2)
        self.layout.addWidget(self.plot, 6, 0, 1, 2)
        self.setLayout(self.layout)

    def adjust_plot(self,  df, time_series):
        """
        Plot DataFrame based on parameter load_profile
        :param time_series:
        :param df: pd.DataFrame
            load_df
        :return: None
        """
        # Create Widgets
        self.plot = Plot(df=df,
                         time_series=time_series,
                         width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.plot, self)
        # Add Widgets to Layout
        self.layout.addWidget(self.plot, 6, 0, 1, 2)
        self.layout.addWidget(self.toolbar, 5, 0, 1, 2)
