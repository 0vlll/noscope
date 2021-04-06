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

        self.animation = qtc.QPropertyAnimation()
        self.fade_animation = qtc.QPropertyAnimation()
        self.unfade_animation = qtc.QPropertyAnimation()
        self.side_menu_toggle_speed = 800
        self.side_menu_swap_speed = 120
        self.easing_curve = qtc.QEasingCurve(qtc.QEasingCurve.Type.OutQuint)

    
        self.ui.splitter.setCollapsible(0, True)
        self.ui.splitter.setCollapsible(1, False)
        
        self.ui.paint_interface = PaintInterface.PaintInterface(self.ui.paint_interface_container)
        self.ui.paint_interface_layout = qtw.QVBoxLayout(self.ui.paint_interface_container)
        self.ui.paint_interface_layout.setSpacing(0)
        self.ui.paint_interface_layout.addWidget(self.ui.paint_interface)
        
        self.ui.scrollArea.verticalScrollBar().setStyleSheet('QScrollBar {width:0px;}')
        self.ui.stackedWidget.setCurrentWidget(self.ui.file_page)
    
        self.ui.file_button.clicked.connect(self.file_information_toggle)
        self.ui.mask_button.clicked.connect(self.mask_settings_toggle)
        self.ui.clip_button.clicked.connect(self.clip_information_toggle)
    
        self.active_project = Project.Project()
        self.ui.save_project_button.clicked.connect(self.save_project)
        self.ui.output_dir_button.clicked.connect(self.set_output_path)
        self.ui.mask_dir_button.clicked.connect(self.set_mask_directory)
        self.ui.image_dir_button.clicked.connect(self.set_clip_directory)
        self.ui.action_open.triggered.connect(self.open_project)
        self.ui.action_save_file.triggered.connect(self.save_project)
        self.ui.action_save_as.triggered.connect(self.save_project_as)

        self.update_settings()

        self.ui.next_frame_button.clicked.connect(lambda: self.ui.frame_slider.setValue(self.ui.frame_slider.value()+1))
        self.ui.previous_frame_button.clicked.connect(lambda: self.ui.frame_slider.setValue(self.ui.frame_slider.value()-1))

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

    def update_settings(self):
        self.ui.frame_slider.setMaximum(self.active_project.get_frame_count())

    def save_project(self):
        if self.active_project.get_project_path() == None:
            file_path = qtw.QFileDialog.getSaveFileName(self, 'Save File', filter='JSON Files (*.json)')
            if file_path[0] == '':
                return
            self.active_project.set_project_path(file_path[0])
            self.active_project.save_project()
        else:
            self.active_project.save_project()
        self.update_settings()

    def save_project_as(self):
        file_path = qtw.QFileDialog.getSaveFileName(self, 'Save File', filter='JSON Files (*.json)')
        if file_path[0] == '':
            return
        self.active_project.set_project_path(file_path[0])
        self.active_project.save_project()
        self.update_settings()


    def open_project(self):
        if self.active_project.is_saved() == False:
            print('not saved')
            ######################### To Be Implemented #########################
        file_path = qtw.QFileDialog.getOpenFileName(self, 'Open File', filter='JSON Files (*.json)')
        if file_path[0] == '':
            return
        self.active_project = Project.Project()    
        self.active_project.open_project(file_path[0])  
        self.update_settings()

    def set_output_path(self):
        file_path = qtw.QFileDialog.getExistingDirectory(self, 'Set Output Directory')
        self.active_project.set_output_path(file_path)

    def set_mask_directory(self):
        file_path = qtw.QFileDialog.getExistingDirectory(self, 'Set Mask Directory')
        self.active_project.set_mask_path(file_path)

    def set_clip_directory(self):
        file_path = qtw.QFileDialog.getExistingDirectory(self, 'Set Clip Directory')
        self.active_project.set_clip_path(file_path)


