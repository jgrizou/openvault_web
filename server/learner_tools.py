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

import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class LearnerManager(object):

    def __init__(self, socketio):
        self.socketio = socketio
        self.n_hypothesis = 10
        self.learners = {}

        self.code_length = 4
        self.code_list = ['' for _ in range(self.code_length)]
        self.code_tmp = ['' for _ in range(self.code_length)]
        self.code_index = 0

    def init(self, room_id):
        self.reset_learner(room_id)
        self.display_grid = ui_tools.push_display(self.socketio, room_id, 2, 5)
        self.code_grid = ui_tools.push_code(self.socketio, room_id, self.code_list)
        self.pad_grid = ui_tools.push_pad(self.socketio, room_id, 3, 3)

        # ask the page if readay to accept flash_patterns
        self.socketio.emit('status', room=room_id)

    def delete(self, room_id):
        del(self.learners[room_id])

    def step(self, room_id, feedback_info=None):
        print(feedback_info)
        if feedback_info is not None:

            displayed_colors = feedback_info['display_colors']
            displayed_flash_patterns = ui_tools.flash_patterns_from_display_colors(displayed_colors)

            if 'key' in feedback_info:
                feedback_symbol = feedback_info['key']
            else:
                feedback_symbol = feedback_info['tile_index']

            self.update_learner(room_id, displayed_flash_patterns, feedback_symbol)

        self.update_flash_pattern(room_id)

        if self.learners[room_id].is_inconsistent():
            print('INCONSISTENT')
        if self.learners[room_id].is_solved():
            print('###########')
            print('###########')
            solution_index = self.learners[room_id].get_solution_index()
            updated_known_symbols = self.learners[room_id].compute_symbols_belief_for_hypothesis(solution_index)
            self.reset_learner(room_id, updated_known_symbols)

            self.code_tmp[self.code_index] = str(solution_index)
            self.code_list[self.code_index] = '#'
            self.code_index += 1

            print(self.code_tmp)

            if self.code_index >= self.code_length:
                self.code_list = ['' for _ in range(self.code_length)]
                self.code_tmp = ['' for _ in range(self.code_length)]
                self.code_index = 0
                self.reset_learner(room_id)

            self.code_grid = ui_tools.push_code(self.socketio, room_id, self.code_list)

            # print(solution_index)
            # print(updated_known_symbols)
            print('###########')
            print('###########')

    def reset_learner(self, room_id, known_symbols={}):
        self.learners[room_id] = DiscreteLearner(self.n_hypothesis, known_symbols)

    def update_learner(self, room_id, flash_patterns, feedback_symbol):
        print('##### Updating {} for {} with {}'.format(room_id, flash_patterns, feedback_symbol))
        self.learners[room_id].update(flash_patterns, feedback_symbol)

    def update_flash_pattern(self, room_id):
        new_flash_pattern = self.learners[room_id].get_next_flash_pattern()
        ui_tools.push_flash_patterns(self.socketio, room_id, self.display_grid, new_flash_pattern)



class LearnerNamespace(Namespace):

    def __init__(self, namespace, learner_manager):
        super().__init__(namespace)
        self.learner_manager = learner_manager

    def on_status(self, status):
        room_id = request.sid
        if status:
            self.learner_manager.step(room_id)
        else:
            emit('status')

    def on_key(self, feedback_info):
        room_id = request.sid
        self.learner_manager.step(room_id, feedback_info)

    def on_click(self, feedback_info):
        room_id = request.sid
        self.learner_manager.step(room_id, feedback_info)
