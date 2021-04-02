from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from UI.MainWindowUI import Ui_MainWindow
from MaskViewer import PaintInterface

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.animation = qtc.QPropertyAnimation()
        self.side_menu_toggle_speed = 800
        self.easing_curve = qtc.QEasingCurve()
        self.easing_curve.setType(qtc.QEasingCurve.Type.OutQuint)

        self.ui.stackedWidget.setCurrentWidget(self.ui.file_page)
        self.ui.paint_interface = PaintInterface.PaintInterface(self.ui.widget_11)
        self.ui.verticalLayout_15 = qtw.QVBoxLayout(self.ui.widget_11)
        self.ui.verticalLayout_15.setSpacing(0)
        self.ui.verticalLayout_15.addWidget(self.ui.paint_interface)
        self.ui.scrollArea.verticalScrollBar().setStyleSheet('QScrollBar {width:0px;}')
        self.ui.file_button.clicked.connect(self.file_information_toggle)
        self.ui.mask_button.clicked.connect(self.mask_settings_toggle)
        self.ui.clip_button.clicked.connect(self.clip_information_toggle)

    def file_information_toggle(self):
        self.animation.stop()
        if self.ui.scrollArea.maximumWidth() <= 125:
            self.ui.stackedWidget.setCurrentWidget(self.ui.file_page)
            self.maximize_side_menu()
        else:
            if self.ui.stackedWidget.currentWidget().objectName() != 'file_page':
                self.set_side_menu(self.ui.file_page)
            else:
                self.minimize_side_menu()
    
    def mask_settings_toggle(self):
        if self.ui.scrollArea.maximumWidth() <= 125:
            self.ui.stackedWidget.setCurrentWidget(self.ui.mask_page)
            self.maximize_side_menu()
        else:
            if self.ui.stackedWidget.currentWidget().objectName() != 'mask_page':
                self.set_side_menu(self.ui.mask_page)
            else:
                self.minimize_side_menu()

    def clip_information_toggle(self):
        self.animation.stop()
        if self.ui.scrollArea.maximumWidth() <= 125:
            self.ui.stackedWidget.setCurrentWidget(self.ui.clip_page)
            self.maximize_side_menu()
        else:
            if self.ui.stackedWidget.currentWidget().objectName() != 'clip_page':
                self.set_side_menu(self.ui.clip_page)
            else:
                self.minimize_side_menu()

    def set_side_menu(self, widget: qtw.QWidget):
        self.ui.stackedWidget.setCurrentWidget(widget)


    
    def minimize_side_menu(self):
        self.animation = qtc.QPropertyAnimation(self.ui.scrollArea, b'maximumWidth')
        self.animation.setEasingCurve(self.easing_curve)
        self.animation.setEndValue(0)
        self.animation.setDuration(self.side_menu_toggle_speed)
        self.animation.start()

    def maximize_side_menu(self):
        self.animation = qtc.QPropertyAnimation(self.ui.scrollArea, b'maximumWidth')
        self.animation.setEasingCurve(self.easing_curve)
        self.animation.setEndValue(250)
        self.animation.setDuration(self.side_menu_toggle_speed)
        self.animation.start()
