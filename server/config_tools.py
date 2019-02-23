import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import json
import copy

import ui_tools
from tools import list_files

CONFIG_FOLDER = os.path.join(HERE_PATH, 'configs')

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


def read_config(config_filename):
    with open(config_filename) as f:
        config = json.load(f)
    return config


def init_state_from_config(config):

    config_copy = copy.deepcopy(config)

    init_state = {}

    ## DISPLAY
    init_state['display_grid'] = ui_tools.build_display_grid(
                                    config_copy['display']['row'],
                                    config_copy['display']['column'])

    ## CODE
    init_state['code'] = config_copy['code']

    ## PAD
    pad_indexes = None
    if 'indexes' in config_copy['pad']:
        pad_indexes = config_copy['pad']['indexes']

    init_state['pad_grid'] = ui_tools.build_pad_grid(
                                    config_copy['pad']['row'],
                                    config_copy['pad']['column'],
                                    pad_indexes)

    # LEARNER
    init_state['learner'] = config_copy['learner']

    return init_state
