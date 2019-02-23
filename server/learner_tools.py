import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding openvault directory to path
import sys
openvault_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(openvault_path)

from flask import request
from flask_socketio import Namespace, emit

from openvault.discrete import DiscreteLearner

import ui_tools
from config_tools import build_config_from_file

import random
import string


class LearnerManager(Namespace):

    def __init__(self, socketio, namespace='/', ):
        super().__init__(namespace)
        self.socketio = socketio
        self.learners = {}

    def spawn(self, room_id, config_filename):
        if room_id in self.learners:
            self.kill(room_id)
        config = build_config_from_file(config_filename)
        self.learners[room_id] = Learner(self.socketio, room_id, config)

    def kill(self, room_id):
        if room_id in self.learners:
            del(self.learners[room_id])

    def on_reset(self):
        room_id = request.sid
        if room_id in self.learners:
            self.learners[room_id].reset()

    def on_status(self, status):
        room_id = request.sid
        if status:
            self.learners[room_id].start()
        else:
            emit('status')

    def on_key(self, feedback_info):
        room_id = request.sid
        self.learners[room_id].step(feedback_info)

    def on_click(self, feedback_info):
        room_id = request.sid
        self.learners[room_id].step(feedback_info)


class Learner(object):

    def __init__(self, socketio, room_id, config):
        self.socketio = socketio
        self.room_id = room_id
        self.config = config
        self.reset()

    def reset(self):
        self.init_learner()
        self.code_manager = CodeManager(self.config['code'])

        # init grid
        ui_tools.push_grid_to_panel(self.socketio, self.room_id,
                                    self.config['display_grid'], 'display')
        ui_tools.push_grid_to_panel(self.socketio, self.room_id,
                                    self.code_manager.code_grid, 'code')
        ui_tools.push_grid_to_panel(self.socketio, self.room_id,
                                    self.config['pad_grid'], 'pad')

        # ask the page if ready to accept flash_patterns
        self.socketio.emit('status', room=self.room_id)

    def init_learner(self):
        learner_info = self.config['learner']
        if learner_info['type'] == 'discrete':
            self.learner = DiscreteLearner(
                learner_info['n_hypothesis'],
                learner_info['known_symbols'])
        else:
            raise Exception('Learner of type {} not handled'. format(learner_info['type']))

    def start(self):
        # starts set the first flash patterns on the display
        self.update_flash_pattern()
        self.update_pad_colors()

    def step(self, feedback_info):
        print(feedback_info)
        if self.code_manager.is_code_decoded():
            print('NOT PROCESSING!')
        else:
            self.update_learner(feedback_info)

            if self.learner.is_inconsistent():
                print('!!!!! INCONSISTENT !!!!!')

            if self.learner.is_solved():
                self.update_code()
                self.update_known_symbols()
                self.update_pad_colors()
                # restart the learner for next number
                self.init_learner()

                print(self.config['learner']['known_symbols'])
                print(self.code_manager.decoded_code)

            if self.code_manager.is_code_decoded():
                print(self.code_manager.secret_code)
                print(self.code_manager.decoded_code)
                if self.code_manager.is_code_valid():
                    print('Amazing!!')
                else:
                    print('Code invalid!!')
            else:
                self.update_flash_pattern()

    def update_flash_pattern(self):
        new_flash_pattern = self.learner.get_next_flash_pattern()

        display_colors = ui_tools.display_colors_from_flash_patterns(self.config['display_grid'], new_flash_pattern)

        ui_tools.push_colors_to_panel(self.socketio, self.room_id, display_colors, 'display')

    def update_learner(self, feedback_info):

        displayed_colors = feedback_info['display_colors']
        displayed_flash_patterns = ui_tools.flash_patterns_from_display_colors(displayed_colors)

        if 'key' in feedback_info:
            feedback_symbol = feedback_info['key']
        else:
            feedback_symbol = feedback_info['tile_index']

        # print('##### Updating {} for {} with {}'.format(self.room_id, displayed_flash_patterns, feedback_symbol))

        self.learner.update(displayed_flash_patterns, feedback_symbol)

    def update_code(self):
        # get new number decoded, add and display resulting code
        # here solution_index is directly the new number
        solution_index = self.learner.get_solution_index()
        self.code_manager.add_new_digit(solution_index)
        ui_tools.push_grid_to_panel(self.socketio, self.room_id,
                                    self.code_manager.code_grid, 'code')

    def update_known_symbols(self):
        # update the known_symbols if needed
        learner_info = self.config['learner']
        if learner_info['accumulate_known_symbols_between_numbers']:
            solution_index = self.learner.get_solution_index()
            learner_info['known_symbols'] = self.learner.compute_symbols_belief_for_hypothesis(solution_index)

    def update_pad_colors(self):
        if self.config['learner']['show_learning_progress']:
            pad_colors = ui_tools.colors_from_index_flash_values(
                self.config['pad_grid'], self.config['learner']['known_symbols'])

            ui_tools.push_colors_to_panel(
                self.socketio, self.room_id,
                pad_colors, 'pad')


class CodeManager(object):

    def __init__(self, code_config):
        self.secret_code = code_config['value']
        self.show_code = code_config['show']
        self.reset()

    def reset(self):
        self.decoded_code = [None for _ in self.secret_code]
        self.ongoing_digit_index = 0

    def add_new_digit(self, digit):
        self.decoded_code[self.ongoing_digit_index] = digit
        self.ongoing_digit_index += 1

    def is_code_decoded(self):
        return not None in self.decoded_code

    def is_code_valid(self):
        return self.secret_code == self.decoded_code

    @property
    def code_grid(self):
        return ui_tools.build_code_grid(self.displayed_code)

    @property
    def displayed_code(self):
        code_list_to_display = []
        for digit in self.decoded_code:
            if digit is None:
                code_list_to_display.append('')
            else:
                if self.show_code:
                    code_list_to_display.append(str(digit))
                else:
                    code_list_to_display.append('#')

        return code_list_to_display
