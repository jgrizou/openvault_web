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

import tools
import ui_tools
import config_tools

import random
import string


class LearnerManager(Namespace):

    def __init__(self, socketio, namespace='/'):
        super().__init__(namespace)
        self.socketio = socketio
        self.learners = {}

    def spawn(self, room_id, config_filename):
        if room_id in self.learners:
            self.kill(room_id)
        config = config_tools.read_config(config_filename)
        self.learners[room_id] = Learner(self.socketio, room_id, config)

    def kill(self, room_id):
        if room_id in self.learners:
            del(self.learners[room_id])

    def on_is_spawn(self):
        room_id = request.sid
        emit('spawn_state', room_id in self.learners)

    def on_reset(self):
        room_id = request.sid
        if room_id in self.learners:
            self.learners[room_id].reset()

    def on_key(self, feedback_info):
        room_id = request.sid
        if room_id in self.learners:
            self.learners[room_id].step(feedback_info)

    def on_click(self, feedback_info):
        room_id = request.sid
        if room_id in self.learners:
            self.learners[room_id].step(feedback_info)

    def on_success(self):
        filename = tools.get_random_file_from_public_path('gifs/yes')
        emit('modal', {'success': True, 'code': '2365', 'gif': filename, 'inconsistent': False})

    def on_fail(self):
        filename = tools.get_random_file_from_public_path('gifs/no')
        emit('modal', {'success': False, 'code': '0000', 'gif': filename, 'inconsistent': True})


class Learner(object):

    def __init__(self, socketio, room_id, config):
        self.socketio = socketio
        self.room_id = room_id
        self.config = config
        self.reset()

    def reset(self):
        self.state = config_tools.init_state_from_config(self.config)
        self.code_manager = CodeManager(self.state['code'])
        self.init_learner()
        self.start()

    def init_learner(self):
        learner_info = self.state['learner']
        if learner_info['type'] == 'discrete':
            self.learner = DiscreteLearner(
                learner_info['n_hypothesis'],
                learner_info['known_symbols'])
        else:
            raise Exception('Learner of type {} not handled'. format(learner_info['type']))

    def start(self):
        self.update_iteration(0)
        self.update_flash_pattern()
        self.update_code()
        self.update_pad()

    def step(self, feedback_info):
        if self.code_manager.is_code_decoded():
            ui_tools.trigger_modal(
                self.socketio,
                self.room_id,
                self.code_manager.is_code_valid(),
                self.learner.is_inconsistent(),
                self.code_manager.decoded_code)
        else:
            self.update_iteration(self.n_iteration + 1)

            self.update_learner(feedback_info)

            if self.learner.is_inconsistent():
                ui_tools.trigger_modal(
                    self.socketio,
                    self.room_id,
                    self.code_manager.is_code_valid(),
                    self.learner.is_inconsistent(),
                    self.code_manager.decoded_code)

            if self.learner.is_solved():
                self.update_code()
                self.update_known_symbols()
                self.update_pad()
                # restart the learner for next number
                self.init_learner()

                print(self.state['learner']['known_symbols'])
                print(self.code_manager.decoded_code)

            if self.code_manager.is_code_decoded():
                ui_tools.trigger_modal(
                    self.socketio,
                    self.room_id,
                    self.code_manager.is_code_valid(),
                    self.learner.is_inconsistent(),
                    self.code_manager.decoded_code)
            else:
                self.update_flash_pattern()

    def update_iteration(self, new_iteration_value):
        self.n_iteration = new_iteration_value
        self.socketio.emit('n_iteration', self.n_iteration, room=self.room_id)

    def update_flash_pattern(self):
        new_flash_pattern = self.learner.get_next_flash_pattern()

        self.state['display_grid'] = ui_tools.build_display_grid(
                                        self.config['display']['row'],
                                        self.config['display']['column'],
                                        new_flash_pattern)

        ui_tools.push_grid_to_panel(self.socketio, self.room_id,
                            self.state['display_grid'], 'display')


    def update_learner(self, feedback_info):

        displayed_grid = feedback_info['display_grid']
        displayed_flash_patterns = ui_tools.flash_patterns_from_displayed_grid(displayed_grid)

        if 'key' in feedback_info:
            feedback_symbol = feedback_info['key']
        else:
            feedback_symbol = feedback_info['tile_index']

        # print('##### Updating {} for {} with {}'.format(self.room_id, displayed_flash_patterns, feedback_symbol))

        self.learner.update(displayed_flash_patterns, feedback_symbol)

    def update_code(self):
        # get new number decoded, add and display resulting code
        # here solution_index is directly the new number
        if self.learner.is_solved():
            solution_index = self.learner.get_solution_index()
            self.code_manager.add_new_digit(solution_index)

        ui_tools.push_grid_to_panel(self.socketio, self.room_id,
                                    self.code_manager.code_grid, 'code')

    def update_known_symbols(self):
        # update the known_symbols if needed
        learner_info = self.state['learner']
        if learner_info['accumulate_known_symbols_between_numbers']:
            solution_index = self.learner.get_solution_index()
            learner_info['known_symbols'] = self.learner.compute_symbols_belief_for_hypothesis(solution_index)

    def update_pad(self):
        learner_info = self.state['learner']
        if learner_info['show_learning_progress']:
            pad_colors = ui_tools.colors_from_index_flash_values(
                self.state['pad_grid'], learner_info['known_symbols'])

            self.state['pad_grid'] = ui_tools.update_grid_colors(
                self.state['pad_grid'],
                pad_colors)

        ui_tools.push_grid_to_panel(
            self.socketio, self.room_id,
            self.state['pad_grid'], 'pad')


class CodeManager(object):

    def __init__(self, code_config):
        self.config =  code_config
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
    def secret_code(self):
        return self.config['secret_code']

    @property
    def code_grid(self):
        grid_layout = None
        if 'grid_layout' in self.config:
            grid_layout = self.config['grid_layout']
        code_grid = ui_tools.build_code_grid(self.displayed_code, grid_layout)
        return code_grid

    @property
    def displayed_code(self):
        code_list_to_display = []
        for digit in self.decoded_code:
            if digit is None:
                code_list_to_display.append('')
            else:
                if self.config['show']:
                    code_list_to_display.append(str(digit))
                else:
                    code_list_to_display.append('#')

        return code_list_to_display
