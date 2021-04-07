from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

class NotSavedDialog(qtw.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent = parent)

        buttons = qtw.QDialogButtonBox.StandardButtons.Save | qtw.QDialogButtonBox.StandardButtons.Cancel

        self.button_box = qtw.QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = qtw.QVBoxLayout(self)
        message = qtw.QLabel('There are unsaved changes in your workspace\nWould you like to save?')
        self.layout.addWidget(message)
        self.layout.addWidget(self.button_box)
        message.setAlignment(qtc.Qt.Alignment.AlignCenter)
        self.setLayout(self.layout)
