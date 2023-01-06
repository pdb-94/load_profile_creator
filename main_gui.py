"""
Module to run the Load Profile Creator (LPC) GUI

@author: Paul Bohn
@contributor: Paul Bohn (TH Köln), Moritz End (TH Köln)
"""

__version__ = '0.1'
__author__ = 'pdb-94'

import sys
from PyQt5.QtWidgets import *
from gui.tab_widget import TabWidget

app = QApplication(sys.argv)
lpc = TabWidget()
sys.exit(app.exec())


