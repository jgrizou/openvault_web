import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import uuid
import time

import tools

LOG_FOLDER = os.path.join(HERE_PATH, 'logs')
MP3_FOLDER_NAME = 'mp3'

def generate_unique_log_folder():
    while True:
        tmp_log_folder = os.path.join(LOG_FOLDER, str(uuid.uuid4()))
        if not os.path.exists(tmp_log_folder):
            break
    tools.ensure_dir(tmp_log_folder)
    return tmp_log_folder

class Logger(object):

    def __init__(self):
        self.log_folder = generate_unique_log_folder()

    def save_mp3(self, mp3_data):
        mp3_folder = os.path.join(self.log_folder, MP3_FOLDER_NAME)
        tools.ensure_dir(mp3_folder)

        files = tools.list_files(mp3_folder, ['*.mp3'])
        mp3_filename = os.path.join(mp3_folder, '{:04}.mp3'.format(len(files)))
        with open(mp3_filename, 'wb') as f:
            f.write(mp3_data)
        return mp3_filename
