import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import json

import ui_tools


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
