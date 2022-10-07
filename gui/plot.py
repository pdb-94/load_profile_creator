"""
Module to display plot in GUI

@author: Paul Bohn
@contributor: Paul Bohn
"""

import sys
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Plot(FigureCanvasQTAgg):

    def __init__(self, df=None, time_series=None, parent=None, width=5, height=4, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)

        super().__init__(fig)
        self.setParent(parent)
        self.df = df
        self.time_series = time_series
        if self.time_series is not None:
            x_axis = self.time_series.dt.strftime('%H:%M')
            self.ax.plot(x_axis, self.df)
            self.ax.set(xlabel='Time HH:MM', ylabel='Power [W]')
