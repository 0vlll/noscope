import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from MainWindow import MainWindow



def open_main_window():
    application = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.setWindowTitle('Noscope')
    application.exec()

open_main_window()