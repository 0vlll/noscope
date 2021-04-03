import json
import os


class Project():
    def __init__(self):
        self._mask_path = None
        self._clip_path = None
        self._output_path = None

    def save_project(self, path):
        project_info = {
            'mask_path': self._mask_path,
            'clip_path': self._clip_path,
            'output_path': self._output_path
        }

        with open(os.path.join(path, 'noscope.json'), 'w') as file:
            json.dump(project_info, file)