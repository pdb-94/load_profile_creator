"""
Module to display plot in GUI

@author: Paul Bohn
@contributor: Paul Bohn
"""

import sys
from PyQt5 import QtCore, QtWidgets
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar


class Plot(FigureCanvasQTAgg):
    """
    Class containing plot
    """

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
