import json
import os


class Project():
    def __init__(self):
        self._mask_path = None
        self._clip_path = None
        self._output_path = None
        self._project_path = None
        self._save_up_to_date = True
        self._clip_frames = 250

    def save_project(self):
        if self._project_path == None:
            return

        project_info = {
            'mask_path': self._mask_path,
            'clip_path': self._clip_path,
            'output_path': self._output_path,
            'project_path': self._project_path
        }

        with open(self._project_path, 'w') as file:
            json.dump(project_info, file)

        self._save_up_to_date = True

    def open_project(self, path):
        file = open(path, 'r')
        data = json.load(file)
        self._mask_path = data['mask_path']
        self._clip_path = data['clip_path']
        self._output_path = data['output_path']
        self._project_path = path
        self._save_up_to_date = True

    def get_project_path(self):
        return self._project_path

    def set_project_path(self, path):
        self._project_path = path

    def set_mask_path(self, path):
        self._mask_path = path
        self.set_not_saved()
    
    def get_mask_path(self):
        return self._mask_path

    def set_clip_path(self, path):
        self._clip_path = path
        self.set_not_saved()

    def get_clip_path(self):
        return self._clip_path

    def set_output_path(self, path):
        self._output_path = path
        self.set_not_saved()

    def get_output_path(self):
        return self._output_path

    def is_saved(self):
        return self._save_up_to_date

    def set_not_saved(self):
        self._save_up_to_date = False

    def set_frame_count(self, frames):
        ######################### Add Implementation for counting and setting #########################
        self._clip_frames = frames

    def get_frame_count(self):
        return self._clip_frames


    