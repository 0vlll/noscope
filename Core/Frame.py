from PIL import Image
from PyQt6 import QtGui as qtg

class Frame:
    def __init__(self, image_path = None, mask_path = None, output_path = None, frame_number = None):
        self._image_path = image_path
        self._mask_path = mask_path
        self._output_path = output_path
        self._frame_number = frame_number
        self._image = None
        self._mask = None
        self._output = None
        self._cached = False

    def load_images(self):
        if self._image_path == None or self._mask_path == None or self._output_path == None:
            return
        try:
            self._image = Image.open(self._image_path)
        except IOError:
            self._image = Image.new('RGB', (10, 10))
            self._image.save(self._image_path)
        try:
            self._mask = Image.open(self._mask_path)
        except IOError:
            self._mask = Image.new('RGB', (10, 10))
            self._mask.save(self._mask_path)
        try:
            self._output = Image.open(self._output_path)
        except IOError:
            self._output = Image.new('RGB', (10, 10))
            self._output.save(self._output_path)        
        
        self._cached = True

    def __str__(self):
        if self._image_path == None or self._mask_path == None or self._output_path == None:
            return "None"
        return self._image_path + " " + self._mask_path + " " + self._output_path
    
    def set_image_path(self, image_path = None):
        self._image_path = image_path

    def set_mask_path(self, mask_path = None):
        self._mask_path = mask_path

    def set_output_path(self, output_path = None):
        self._output_path = output_path

    def set_frame_number(self, frame_number = None):
        self._frame_number = frame_number
    
    def get_image(self):
        return self._image

    def set_image(self, image):
        if image == None:
            return
        self._image = image

    def get_mask(self):
        return self._mask

    def set_mask(self, mask):
        if mask == None:
            return
        self._mask = mask

    def get_output(self):
        return self._output

    def set_output(self, output):
        if output == None:
            return
        self._output = output

    def get_image_pixmap(self):
        return self._pil_to_qt(self._image)

    def get_mask_pixmap(self):
        return self._pil_to_qt(self._mask)

    def get_output_pixmap(self):
        return self._pil_to_qt(self._output)

    def get_image_path(self):
        return self._image_path
    
    def get_mask_path(self):
        return self._mask_path

    def get_ouput_path(self):
        return self._output_path

    def get_frame_number(self):
        return self._frame_number

    def _pil_to_qt(self, image):
        if image.mode == "RGB":
            r, g, b = image.split()
            image = Image.merge("RGB", (b, g, r))
        elif image.mode == "RGBA":
            r, g, b, a = image.split()
            image = Image.merge("RGBA", (b, g, r, a))
        elif image.mode == "L":
            image = image.convert("RGBA")
        converted_image = image.convert("RGBA")
        data = converted_image.tobytes("raw", "RGBA")
        qim = qtg.QImage(data, image.size[0], image.size[1], qtg.QImage.Format.Format_ARGB32)
        pixmap = qtg.QPixmap.fromImage(qim)
        return pixmap
    
    def is_cached(self):
        return self._cached
    
    def uncache(self):
        self._image = None
        self._output = None
        self._mask = None
        self._cached = False

    def save_output(self):
        if self._output == None:
            return
        self._output.save(self._output_path)