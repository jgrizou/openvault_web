import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import json

import ui_tools
from tools import list_files

CONFIG_FOLDER = os.path.join(HERE_PATH, 'configs')

def get_configs():
    config_files = list_files(CONFIG_FOLDER, ['*.json'])
    config_files.sort()

    configs = []
    for config_filename in config_files:
        config_data = read_config(config_filename)
        config_info = {}
        config_info['filename'] = os.path.relpath(config_filename, CONFIG_FOLDER)
        config_info['message'] = config_data['name']
        configs.append(config_info)
    return configs


def read_config(config_filename):
    with open(config_filename) as f:
        config_data = json.load(f)
    return config_data


def build_config_from_file(config_filename):
    return build_config(read_config(config_filename))


def build_config(config_data):
    config = {}

    ## DISPLAY
    display_indexes = None
    if 'indexes' in config_data['display']:
        display_indexes = config_data['display']['indexes']

    config['display_grid'] = ui_tools.build_display_grid(
                                    config_data['display']['row'],
                                    config_data['display']['column'],
                                    display_indexes)

    ## PAD
    pad_indexes = None
    if 'indexes' in config_data['pad']:
        pad_indexes = config_data['pad']['indexes']

    config['pad_grid'] = ui_tools.build_pad_grid(
                                    config_data['pad']['row'],
                                    config_data['pad']['column'],
                                    pad_indexes)

    if 'colors' in config_data['pad']:
        config['pad_colors'] = config_data['pad']['colors']

    ## CODE
    config['code'] = config_data['code']

    # LEARNER
    config['learner'] = config_data['learner']

    return config
