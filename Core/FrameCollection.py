from PyQt6 import QtCore as qtc
from PIL import Image
from .Frame import Frame
from .Grabcut import generate_grabcut
from os import listdir
import os
import io
import _thread


class FrameCollection:
    def __init__(self, image_directory = None, mask_directory = None, output_directory = None):
        self._frames = []
        self._image_directory = image_directory
        self._mask_directory = mask_directory
        self._output_directory = output_directory
        self._cached = []
        self._max_cached = 100

    def load_frames(self):
        self._cached = []
        if self._image_directory == None or self._mask_directory == None or self._output_directory == None:
            return
        images = listdir(self._image_directory)
        masks = listdir(self._mask_directory)

        for mask in masks:
            for image in images:
                if self._get_file_name(mask) == self._get_file_name(image):
                    frame_number = ''
                    for i in image:
                        if i.isdigit():
                            frame_number += i
                    frame = Frame(os.path.join(self._image_directory, image), os.path.join(self._mask_directory, mask), os.path.join(self._output_directory, mask), int(frame_number))
                    if len(self._frames) != 0:
                        largest = True
                        for i in range(0, len(self._frames)):
                            if self._frames[i].get_frame_number() >= frame.get_frame_number():
                                self._frames.insert(i, frame)
                                largest = False
                                break
                        
                        if largest:
                            self._frames.append(frame)
                    else:
                        self._frames.append(frame) 
        
    def cache_frame(self, index: int = None):
        if index == None or index >= len(self._frames):
            return
        self._frames[index].load_images()
        self._cached.insert(0, index)
        if len(self._cached) > self._max_cached and len(self._cached) > 0:
            index = self._cached.pop()
            self._frames[index].uncache()

    def set_frame_directories(self, image_directory = None, mask_directory = None, output_directory = None):
        self._image_directory = image_directory
        self._mask_directory = mask_directory
        self._output_directory = output_directory

    def _get_file_name(self, file_name):
        index = file_name[:file_name.find('.')]
        if (index != -1):
            return index
        else:
            return file_name

    def get_frame_count(self):
        if len(self._frames) == None:
            return 0
        return len(self._frames)

    def get_frame_pixmap(self, frame_index):
        return self._frames[frame_index].get_image_pixmap(), self._frames[frame_index].get_output_pixmap()

    def get_frame(self, index: int):
        if (index >= len(self._frames)):
            return 
        return self._frames[index]

    def set_image_directory(self, path = None):
        if path == None: 
            return
        self._image_directory = path
        self.load_frames()

    def set_output_directory(self, path = None):
        if path == None: 
            return
        self._output_directory = path
        self.load_frames()

    def set_mask_directory(self, path = None):
        if path == None: 
            return
        self._mask_directory = path
        self.load_frames()

    def get_image_directory(self):
        return self._image_directory

    def get_mask_directory(self):
        return self._mask_directory

    def get_output_directory(self):
        return self._output_directory
    
    def update_mask(self, index, buffer: qtc.QBuffer):
        if index == None or buffer == None or index < 0 or index - 1 > len(self._frames):
            return
        mask = Image.open(io.BytesIO(buffer.data()))
        self._frames[index].set_mask(mask)

    def update_image(self, index, buffer: qtc.QBuffer):
        if index == None or buffer == None or index < 0 or index - 1 > len(self._frames):
            return
        image = Image.open(io.BytesIO(buffer.data()))
        self._frames[index].set_image(image)

    def update_output(self, index, buffer: qtc.QBuffer):
        if index == None or buffer == None or index < 0 or index - 1 > len(self._frames):
            return
        output = Image.open(io.BytesIO(buffer.data()))
        self._frames[index].set_output(output)

    def generate_single_output(self, index = None):
        if index == None or index < 0 or index >= len(self._frames) or self._frames[index] == None:
            return
        frame = self._frames[index]
        frame.load_images()
        print(self._frames[index])
        (output, time) = generate_grabcut(frame.get_mask().convert('L'), frame.get_image())
        frame.set_output(Image.fromarray(output))
        frame.save_output()
        print('finished frame in ' + str(time))
        frame.uncache()

    
 