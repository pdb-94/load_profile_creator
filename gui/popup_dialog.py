import sys
from PyQt5.QtWidgets import *


class DeleteDialog(QMessageBox):
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


class Load_Dialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Load Generator')

        # Labels
        self.label = QLabel('')
        self.name = QLabel('Name')

        # Edits
        self.name_edit = QLineEdit()

        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0, 1, 2)
        self.layout.addWidget(self.name, 1, 0)
        self.layout.addWidget(self.name_edit, 1, 1)
        self.setLayout(self.layout)

        self.show()

    def constant(self):
        self.label.setText('Constant Load')

    def sequential(self):
        self.label.setText('Sequential Load')

    def database(self):
        self.label.setText('Data base Load')

    def user(self):
        self.label.setText('User Load')
