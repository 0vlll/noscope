from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from ImageContainer import ImageContainer

class PaintInterface(qtw.QScrollArea):
    def __init__(self, parent):
        super().__init__(parent = parent)
