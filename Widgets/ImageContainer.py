from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

class ImageContainer(qtw.QLabel):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # Container Pixmaps # 

        self.setPixmap(qtg.QPixmap(0, 0))
        
        self._master_pixmap = None
        self._original_pixmap = None

        # Pixmap Attributes # 

        self._opacity = 1
        self._max_dimension = None

        # Widget Attributes # 

        self._last_x = None
        self._last_y = None

        self._scroll_quality = 5
        self._pen_size = 10
        self._pen_color = qtg.QColor(0, 0, 0)
    
    def load_pixmap(self, pixmap: qtg.QPixmap):
        self.setPixmap(pixmap)
        self._master_pixmap = qtg.QPixmap(pixmap)
        self._original_pixmap = qtg.QPixmap(pixmap)

        if self._max_dimension == None:
            self._max_dimension = max(pixmap.width(), pixmap.height())
    
    def unload_pixmap(self):
        self.setPixmap(qtg.QPixmap())
        self._master_pixmap = None
        self._original_pixmap = None

    def update_pixmap(self):
        if self._master_pixmap == None:
            return
        scaled = self._master_pixmap.scaled(self._max_dimension, self._max_dimension, qtc.Qt.KeepAspectRatio)
        updated = qtg.QPixmap(scaled)
        updated.full(qtc.Qt.transparent)
        painter = qtg.QPainter(updated)
        painter.setOpacity(self._opacity)
        painter.drawPixmap(0, 0, scaled)
        painter.end()
        self.setPixmap(updated)

    def reset_pixmap(self):
        self._master_pixmap = qtg.QPixmap(self._original_pixmap)
        self.update_pixmap()
        
    def get_master_pixmap(self):
        return self._master_pixmap

    def set_opacity(self, value):
        if self._master_pixmap == None or value > 1 or value < 0:
            return
        self._opacity = value

    def set_brush_size(self, value):
        self._pen_size = value

    def set_brush_color(self, color):
        if not isinstance(color, qtg.QColor):
            return
        self._pen_color = color

    def set_zoom(self, dimension):
        self._max_dimension = dimension

    # Events #

    def mouseMoveEvent(self, e):
        if self._master_pixmap == None:
            return
        if e.buttons() != qtc.Qt.LeftButton:
            e.ignore()
        ratio = self.pixmap().width() / self._master_pixmap.width()
        mouse_x = e.x()
        mouse_y = e.y()
        if self.pixmap().height() <= self._master_pixmap.height():
            mouse_y = e.y() - (self.height()-self.pixmap().height())/2
        if self._last_x == None or self._last_y == None:
            self._last_x = mouse_x
            self._last_y = mouse_y
        
        # update pixmap

        view_painter = qtg.QPainter(self.pixmap())
        view_pen = view_painter.pen()
        view_pen.setWidth(self._pen_size * ratio)
        view_pen.setColor(self._pen_color)
        view_painter.setPen(view_pen)
        view_painter.drawLine(self._last_x, self._last_y, mouse_x, mouse_y)
        view_painter.end()
        
        master_painter = qtg.QPainter(self.pixmap())
        master_pen = master_painter.pen()
        master_pen.setWidth(self._pen_size)
        master_pen.setColor(self._pen_color)
        master_painter.setPen(master_pen)
        master_painter.drawLine(self._last_x / ratio, self._last_y / ratio, mouse_x / ratio, mouse_y / ratio)
        master_painter.end()

        self.update()
        self.update_pixmap()

        self._last_x = mouse_x
        self._last_y = mouse_y

    def mouseReleaseEvent(self, e):
        self._last_x = None
        self._last_y = None