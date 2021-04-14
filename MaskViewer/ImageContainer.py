from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

class ImageContainer(qtw.QLabel):
    def __init__(self, parent = None):
        super().__init__(parent = parent)

        # Container Pixmaps # 

        self.setPixmap(qtg.QPixmap(0, 0))
        
        self._master_pixmap = None
        self._original_pixmap = None

        # Pixmap Attributes # 

        self._opacity = 1
        self._max_pixmap_dimension = None
        self._output_changed = False

        # Widget Attributes # 

        self._last_x = None
        self._last_y = None

        self._scroll_quality = 5
        self._pen_size = 10
        self._pen_color = qtg.QColor(0, 0, 0)
    
    def load_pixmap(self, pixmap: qtg.QPixmap):
        self._output_changed = False
        self.setPixmap(pixmap)
        self._master_pixmap = qtg.QPixmap(pixmap)
        self._original_pixmap = qtg.QPixmap(pixmap)

        if self._max_pixmap_dimension == None:
            self._max_pixmap_dimension = max(pixmap.width(), pixmap.height())
        self.update_pixmap()
    
    def unload_pixmap(self):
        self.setPixmap(qtg.QPixmap())
        self._master_pixmap = None
        self._original_pixmap = None

    def update_pixmap(self):
        if self._master_pixmap == None or self.pixmap().width() == 0 or self.pixmap().height() == 0:
            return
        scaled = self._master_pixmap.scaled(self._max_pixmap_dimension, self._max_pixmap_dimension, qtc.Qt.AspectRatioMode.KeepAspectRatio)
        updated = qtg.QPixmap(scaled)
        updated.fill(qtc.Qt.GlobalColor.transparent)
        painter = qtg.QPainter(updated)
        painter.setOpacity(self._opacity)
        painter.drawPixmap(0, 0, scaled)
        painter.end()
        self.setPixmap(updated)

    def reset_pixmap(self):
        self._master_pixmap = qtg.QPixmap(self._original_pixmap)
        self.update_pixmap()

    def paint_pixmaps(self, mouse_x, mouse_y, ratio):
        view_pixmap = qtg.QPixmap(self.pixmap())
        view_painter = qtg.QPainter(view_pixmap)
        view_pen = view_painter.pen()
        view_pen.setWidth(self._pen_size * ratio)
        view_pen.setColor(self._pen_color)
        view_painter.setPen(view_pen)
        view_painter.drawLine(self._last_x, self._last_y, mouse_x, mouse_y)
        view_painter.end() 
        self.setPixmap(view_pixmap)
        
        master_pixmap = qtg.QPixmap(self._master_pixmap)
        master_painter = qtg.QPainter(master_pixmap)
        master_pen = master_painter.pen()
        master_pen.setWidth(self._pen_size)
        master_pen.setColor(self._pen_color)
        master_painter.setPen(master_pen)
        master_painter.drawLine(self._last_x / ratio, self._last_y / ratio, mouse_x / ratio, mouse_y / ratio)
        master_painter.end()
        self._master_pixmap = qtg.QPixmap(master_pixmap)
        self._output_changed = True
        
    def get_master_pixmap(self):
        return self._master_pixmap

    def set_opacity(self, value):
        if value > 1 or value < 0:
            return
        self._opacity = value
        self.update_pixmap()

    def set_pen_size(self, value):
        if value < 1: 
            return
        self._pen_size = value

    def set_pen_color(self, color):
        if not isinstance(color, qtg.QColor):
            return
        self._pen_color = color

    def set_zoom(self, dimension):
        self._max_pixmap_dimension = dimension
        self.update_pixmap()

    def output_changed(self):
        return self._output_changed

    # Events #

    def mouseMoveEvent(self, e):
        if self._master_pixmap == None or self.pixmap().width() == 0 or self.pixmap().height() == 0:
            return
        if e.buttons() != qtc.Qt.MouseButtons.LeftButton:
            e.ignore()
            return
        ratio = self.pixmap().width() / self._master_pixmap.width()
        mouse_x = e.position().x()
        mouse_y = e.position().y()
        if self.pixmap().height() <= self._master_pixmap.height():
            mouse_y = e.position().y() - (self.height()-self.pixmap().height())/2
        if self._last_x == None or self._last_y == None:
            self._last_x = mouse_x
            self._last_y = mouse_y
        
        self.paint_pixmaps(mouse_x, mouse_y, ratio)
        
        self.update()
        self.update_pixmap()

        self._last_x = mouse_x
        self._last_y = mouse_y

    def mouseReleaseEvent(self, e):
        self._last_x = None
        self._last_y = None
        e.ignore()