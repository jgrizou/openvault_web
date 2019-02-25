import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import fnmatch
import random

# say the server where to serve the static files
SERVER_FOLDER=os.path.normpath(os.path.join(HERE_PATH, '../client/dist'))


def get_random_file_from_public_path(path):
    folderpath = os.path.join(SERVER_FOLDER, path)
    all_files = list_files(folderpath, ['*.gif'])
    selected_file = random.choice(all_files)
    rel_path = os.path.relpath(selected_file, SERVER_FOLDER)
    return rel_path


def list_files(path='.', patterns=['*'], min_depth=0, max_depth=float('inf')):
    if type(patterns) == str:
        patterns = [patterns]
    found_files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            filedir = os.path.abspath(dirpath)
            filepath = os.path.join(filedir, filename)
            depth = filepath[len(os.path.abspath(path)) + len(os.path.sep):].count(os.path.sep)
            if min_depth <= depth <= max_depth:
                for pattern in patterns:
                    if fnmatch.fnmatch(filename, pattern):
                        found_files.append(filepath)
    return found_files
