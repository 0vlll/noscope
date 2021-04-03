from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from UI.MainWindowUI import Ui_MainWindow
from MaskViewer import PaintInterface
from Core import Project

MIN_SIZE, MAX_SIZE = 0, 16777215

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._set_animation_properties()
        self._set_interface_properties()
        self._connect_side_menu_toggle_events()
        self._set_project_properties()

    def _set_animation_properties(self):
        self.animation = qtc.QPropertyAnimation()
        self.fade_animation = qtc.QPropertyAnimation()
        self.unfade_animation = qtc.QPropertyAnimation()
        self.side_menu_toggle_speed = 800
        self.side_menu_swap_speed = 120
        self.easing_curve = qtc.QEasingCurve(qtc.QEasingCurve.Type.OutQuint)

    def _set_interface_properties(self):
        self.ui.splitter.setCollapsible(0, True)
        self.ui.splitter.setCollapsible(1, False)
        
        self.ui.paint_interface = PaintInterface.PaintInterface(self.ui.paint_interface_container)
        self.ui.paint_interface_layout = qtw.QVBoxLayout(self.ui.paint_interface_container)
        self.ui.paint_interface_layout.setSpacing(0)
        self.ui.paint_interface_layout.addWidget(self.ui.paint_interface)
        
        self.ui.scrollArea.verticalScrollBar().setStyleSheet('QScrollBar {width:0px;}')
        self.ui.stackedWidget.setCurrentWidget(self.ui.file_page)

    def _connect_side_menu_toggle_events(self):
        self.ui.file_button.clicked.connect(self.file_information_toggle)
        self.ui.mask_button.clicked.connect(self.mask_settings_toggle)
        self.ui.clip_button.clicked.connect(self.clip_information_toggle)

    def _set_project_properties(self):
        self.active_project = None
        self.ui.save_project_button.clicked.connect(self.save_project)

    ######################### Side Menu Toggle #########################

    def file_information_toggle(self):
        if self.ui.scrollArea.width() <= 125:
            self.ui.stackedWidget.setCurrentWidget(self.ui.file_page)
            self.toggle_side_menu()
        else:
            if self.ui.stackedWidget.currentWidget().objectName() != 'file_page':
                self.fade_swap_page(self.ui.file_page)
            else:
                self.toggle_side_menu()
    
    def mask_settings_toggle(self):
        if self.ui.scrollArea.width() <= 125:
            self.ui.stackedWidget.setCurrentWidget(self.ui.mask_page)
            self.toggle_side_menu()
        else:
            if self.ui.stackedWidget.currentWidget().objectName() != 'mask_page':
                self.fade_swap_page(self.ui.mask_page)
            else:
                self.toggle_side_menu()

    def clip_information_toggle(self):
        if self.ui.scrollArea.width() <= 125:
            self.ui.stackedWidget.setCurrentWidget(self.ui.clip_page)
            self.toggle_side_menu()
        else:
            if self.ui.stackedWidget.currentWidget().objectName() != 'clip_page':
                self.fade_swap_page(self.ui.clip_page)
            else:
                self.toggle_side_menu()

    def fade_swap_page(self, widget: qtw.QWidget):
        opacity = qtw.QGraphicsOpacityEffect(self.ui.scrollArea)
        self.ui.scrollArea.setGraphicsEffect(opacity)
        self.fade_animation = qtc.QPropertyAnimation(opacity, b'opacity')
        self.fade_animation.setDuration(self.side_menu_swap_speed)
        self.fade_animation.setEndValue(0)
        self.fade_animation.setStartValue(1)
        self.fade_animation.start()
        self.unfade_animation = qtc.QPropertyAnimation(opacity, b'opacity')
        self.unfade_animation.setDuration(self.side_menu_swap_speed)
        self.unfade_animation.setEndValue(1)
        self.unfade_animation.setStartValue(0)
        self.fade_animation.finished.connect(lambda: self.ui.stackedWidget.setCurrentWidget(widget))
        self.fade_animation.finished.connect(lambda: self.unfade_animation.start())

    def toggle_side_menu(self):
        self.animation = qtc.QVariantAnimation()
        self.animation.setDuration(self.side_menu_toggle_speed)
        self.animation.setEasingCurve(self.easing_curve)

        if self.ui.scrollArea.width() > 250:
            self.animation.setEndValue(250)
            self.animation.setStartValue(self.ui.splitter.sizes()[0])
        elif self.ui.scrollArea.width() <= 125:
            self.animation.setEndValue(250)
            self.animation.setStartValue(MIN_SIZE)
        else:
            self.animation.setEndValue(MIN_SIZE)
            self.animation.setStartValue(self.ui.splitter.sizes()[0])
        self.animation.valueChanged.connect(self.onValueChanged)
        self.animation.start()        

    def onValueChanged(self, value):
        self.ui.scrollArea.setMaximumWidth(value)
        self.ui.splitter.setSizes([value, self.ui.splitter.sizes()[1]])
        self.animation.finished.connect(lambda: self.ui.splitter.setSizes(self.ui.splitter.sizes()))
        self.animation.finished.connect(lambda: self.ui.scrollArea.setMaximumWidth(MAX_SIZE))

    ######################### Project Operations #########################

    def save_project(self):
        file_path = qtw.QFileDialog.getExistingDirectory(self)
        self.active_project = Project.Project()
        self.active_project.save_project(file_path)
        

