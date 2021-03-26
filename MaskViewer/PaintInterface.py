from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from .ImageContainer import ImageContainer

class PaintInterface(qtw.QScrollArea):
    def __init__(self, parent):
        super().__init__(parent = parent)

        self._mouse_last_x = None
        self._mouse_last_y = None
        self._zoom_last_x = None
        self._zoom_last_y = None

        self._max_pixmap_dimension = None
        self._last_midpoint = None
        self._panning_sensitivity = 1
        self._zoom_interval = 25

        self.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        self.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
        self.setWidgetResizable(True)
        self.setAlignment(qtc.Qt.Alignment.AlignCenter)

        # setting content widget
        self.contents = qtw.QWidget()
        self.setWidget(self.contents)

        # creating stacked layout
        self.stacked_layout = qtw.QStackedLayout(self.contents)
        self.contents.setLayout(self.stacked_layout)
        self.stacked_layout.setStackingMode(qtw.QStackedLayout.StackingMode.StackAll)
        self.setAlignment(qtc.Qt.Alignment.AlignCenter)

        # creating top layer
        self.top_layer = qtw.QWidget(self.contents)
        self.stacked_layout.addWidget(self.top_layer)
        self.top_vertical_layout = qtw.QVBoxLayout(self.top_layer)
        self.top_layer.setStyleSheet('background-color: rgba(0, 0, 0, 0);')

        # creating top image container
        self.top_container = ImageContainer(self.top_layer)
        self.top_vertical_layout.addWidget(self.top_container)
        self.top_container.setStyleSheet('background-color: rgba(0, 0, 0, 0);')

        # creating backdrop layer
        self.backdrop_layer = qtw.QWidget(self.contents)
        self.stacked_layout.addWidget(self.backdrop_layer)
        self.backdrop_vertical_layout = qtw.QVBoxLayout(self.backdrop_layer)
        self.backdrop_layer.setStyleSheet('background-color: rgba(0, 0, 0, 0);')

        # creating backdrop image container
        self.backdrop_container = ImageContainer(self.backdrop_layer)
        self.backdrop_vertical_layout.addWidget(self.backdrop_container)
        self.backdrop_container.setStyleSheet('background-color: rgba(0, 0, 0, 0);')

    def load_pixmaps(self, mask: qtg.QPixmap, image: qtg.QPixmap):
        self.top_container.load_pixmap(mask)
        self.backdrop_container.load_pixmap(image)
        self._max_pixmap_dimension = max(mask.width(), mask.height())
        self._last_midpoint = qtc.QPoint(self.horizontalScrollBar().value() + self.width() / 2, self.verticalScrollBar().value()+self.height() / 2)

    def unload_pixmaps(self):
        self.top_container.unload_pixmap()
        self.backdrop_container.unload_pixmap()

    def get_mask(self):
        return self.top_container.get_master_pixmap()

    def set_opacity(self, value):
        self.top_container.set_opacity(value)

    def set_pen_size(self, value):
        self.top_container.set_pen_size(value)

    def set_pen_color(self, color: qtg.QColor):
        self.top_container.set_pen_color(color)

    def set_zoom(self):
        if (self._zoom_last_x == None or self._zoom_last_y == None 
            or self._zoom_last_x == 0 or self._zoom_last_y == 0):
            return

        self.top_container.set_zoom(self._max_pixmap_dimension)
        zoom_change_x = self.top_container.pixmap().width() / self._zoom_last_x
        self.backdrop_container.set_zoom(self._max_pixmap_dimension)
        zoom_change_y = self.top_container.pixmap().height() / self._zoom_last_y

        
        scaled_midpoint = qtc.QPoint(self._last_midpoint.x() * zoom_change_x, self._last_midpoint.y() * zoom_change_y)
        self.horizontalScrollBar().setValue(round(self.horizontalScrollBar().value() + scaled_midpoint.x() - self._last_midpoint.x()))
        self.verticalScrollBar().setValue(round(self.verticalScrollBar().value() + scaled_midpoint.y() - self._last_midpoint.y()))
        
        self._last_midpoint.setX(self.horizontalScrollBar().value() + self.width() / 2) 
        self._last_midpoint.setY(self.verticalScrollBar().value() + self.height() / 2)

    # Events #

    def mouseMoveEvent(self, e):
        if (e.buttons()!=qtc.Qt.MouseButtons.LeftButton and e.buttons()!=qtc.Qt.MouseButtons.RightButton) or (e.buttons()==qtc.Qt.MouseButtons.LeftButton and qtw.QApplication.keyboardModifiers()==qtc.Qt.KeyboardModifiers.ControlModifier):
            if self._mouse_last_x == None or self._mouse_last_y == None:
                self._mouse_last_x = e.position().x()
                self._mouse_last_y = e.position().y() 
            x_scroll_value = (self._mouse_last_x-e.position().x()) * self._panning_sensitivity + self.horizontalScrollBar().value() 
            y_scroll_value = (self._mouse_last_y-e.position().y()) * self._panning_sensitivity + self.verticalScrollBar().value()

            self.horizontalScrollBar().setValue(x_scroll_value)
            self.verticalScrollBar().setValue(y_scroll_value)
            self._mouse_last_x = e.position().x()
            self._mouse_last_y = e.position().y()
            self._last_midpoint.setX(self.horizontalScrollBar().value()+self.width() / 2) 
            self._last_midpoint.setY(self.verticalScrollBar().value()+self.height() / 2)
            e.ignore()
        
            
        
    def mouseReleaseEvent(self, e):
        self._mouse_last_x = None
        self._mouse_last_y = None


    def wheelEvent(self, e):
        e.ignore()
        if self._max_pixmap_dimension == None:
            return
        if self._zoom_last_x == None or self._zoom_last_y == None:
            self._zoom_last_x = self.top_container.pixmap().width()
            self._zoom_last_y = self.top_container.pixmap().height()
        if e.angleDelta().y() > 0 and self._max_pixmap_dimension - self._zoom_interval > 0:
            self._max_pixmap_dimension -= self._zoom_interval
        else:
            self._max_pixmap_dimension += self._zoom_interval

        self.set_zoom()
        self._zoom_last_x = self.top_container.pixmap().width()
        self._zoom_last_y = self.top_container.pixmap().height()
        self.top_container.update_pixmap()
        self.backdrop_container.update_pixmap()