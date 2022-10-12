"""
Module to display plot in GUI

@author: Paul Bohn
@contributor: Paul Bohn
"""

import datetime as dt
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

# TODO: show time on x-axis not date


class Plot(FigureCanvasQTAgg):
    """
    Class containing plot
    """
    def __init__(self, df: pd.Series = None, time_series: pd.Series = None, parent=None, width=5, height=4, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)

        super().__init__(fig)
        self.setParent(parent)
        self.df = df
        self.time_series = time_series
        if self.time_series is not None:
            self.ax.plot(self.time_series, self.df)
            x_ticks = np.arange(self.time_series.iloc[0],
                                self.time_series.iloc[-1]+dt.timedelta(hours=2),
                                dt.timedelta(hours=2)).astype(dt.datetime)
            self.ax.set(xlabel='Time [HH:MM]', ylabel='Power [W]')
            plt.xticks(x_ticks, rotation=45)
