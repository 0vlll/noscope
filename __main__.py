import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from UI.MainWindow import Ui_MainWindow
from MaskViewer import PaintInterface

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.stackedWidget.setCurrentWidget(self.ui.file_page)
        self.ui.paint_interface = PaintInterface.PaintInterface(self.ui.widget_11)
        self.ui.verticalLayout_15.addWidget(self.ui.paint_interface)
        self.ui.scrollArea.verticalScrollBar().setStyleSheet('QScrollBar {width:0px;}')
        self.ui.file_button.clicked.connect(self.file_information_toggle)
        self.ui.mask_button.clicked.connect(self.mask_settings_toggle)
        self.ui.clip_button.clicked.connect(self.clip_information_toggle)

    def file_information_toggle(self):
        if self.ui.scrollArea.maximumWidth() != 250:
            self.ui.stackedWidget.setCurrentWidget(self.ui.file_page)
            self.maximize_side_menu()
        else:
            if self.ui.stackedWidget.currentWidget().objectName() != 'file_page':
                self.set_side_menu(self.ui.file_page)
            else:
                self.minimize_side_menu()
    
    def mask_settings_toggle(self):
        if self.ui.scrollArea.maximumWidth() != 250:
            self.ui.stackedWidget.setCurrentWidget(self.ui.mask_page)
            self.maximize_side_menu()
        else:
            if self.ui.stackedWidget.currentWidget().objectName() != 'mask_page':
                self.set_side_menu(self.ui.mask_page)
            else:
                self.minimize_side_menu()

    def clip_information_toggle(self):
        if self.ui.scrollArea.maximumWidth() != 250:
            self.ui.stackedWidget.setCurrentWidget(self.ui.clip_page)
            self.maximize_side_menu()
        else:
            if self.ui.stackedWidget.currentWidget().objectName() != 'clip_page':
                self.set_side_menu(self.ui.clip_page)
            else:
                self.minimize_side_menu()

    def set_side_menu(self, widget: qtw.QWidget):
        opacity = qtw.QGraphicsOpacityEffect(self.ui.stackedWidget)
        self.ui.stackedWidget.setGraphicsEffect(opacity)
        self.animation = qtc.QPropertyAnimation(opacity, b'opacity')
        self.animation.setEndValue(0)
        self.animation.setDuration(100)
        self.animation.start()
        self.animation.finished.connect(lambda: self.ui.stackedWidget.setCurrentWidget(widget))
        self.animation.finished.connect(lambda: self.set_side_menu_opaque(opacity))
        
    def set_side_menu_opaque(self, graphics_effect):
        self.animation = qtc.QPropertyAnimation(graphics_effect, b'opacity')
        self.animation.setEndValue(1)
        self.animation.setDuration(100)
        self.animation.start()
    
    def minimize_side_menu(self):
        self.animation = qtc.QPropertyAnimation(self.ui.scrollArea, b'maximumWidth')
        self.animation.setEndValue(0)
        self.animation.setDuration(250)
        self.animation.start()

    def maximize_side_menu(self):
        self.animation = qtc.QPropertyAnimation(self.ui.scrollArea, b'maximumWidth')
        self.animation.setEndValue(250)
        self.animation.setDuration(250)
        self.animation.start()





def open_main_window():
    application = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    application.exec()

open_main_window()