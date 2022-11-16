"""
Module with GUI PopUps

@author: Paul Bohn
@contributor: Paul Bohn
"""

from PyQt5.QtWidgets import *


class DeleteDialog(QMessageBox):
    """
    Warning PopUp DIalog
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Information)
        self.setText("Deleting all project progressions. Continue deleting?")
        self.setWindowTitle("Warning")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    def execute(self):
        self.exec_()
        if self.clickedButton() is self.button(QMessageBox.Yes):
            return True
        elif self.clickedButton() is self.button(QMessageBox.No):
            return False
        return None
