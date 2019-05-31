import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import fnmatch
import json

# say the server where to serve the static files
SERVE_FOLDER=os.path.normpath(os.path.join(HERE_PATH, '../client/dist'))
CONFIG_FOLDER = os.path.join(HERE_PATH, 'configs')


def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)


def read_config(config_filename):
    with open(config_filename) as f:
        config = json.load(f)
    return config

def get_configs():
    config_files = list_files(CONFIG_FOLDER, ['*.json'])
    config_files.sort()

    configs = []
    for config_filename in config_files:
        config = read_config(config_filename)
        config_info = {}
        config_info['filename'] = os.path.relpath(config_filename, CONFIG_FOLDER)
        config_info['message'] = config['name']
        configs.append(config_info)
    return configs

def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

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
