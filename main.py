"""
Main module to run Load Profile Creator (LPC)

@author: Paul Bohn
@contributor: Paul Bohn, Moritz End
"""

__version__ = '0.1'
__author__ = 'pdb-94'

import sys
from PyQt5.QtWidgets import *
from gui.tab_widget import TabWidget


app = QApplication(sys.argv)
lpc = TabWidget()
sys.exit(app.exec())
