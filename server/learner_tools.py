import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding openvault directory to path
import sys
openvault_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(openvault_path)

import time

import base64

from flask import request
from flask_socketio import Namespace, emit

from tools import CONFIG_FOLDER, read_config
from logging_tools import Logger

from openvault import classifier_tools
from openvault.discrete import DiscreteLearner
from openvault.continuous import ContinuousLearner

from audio_features.openvault_tools import AudioVaultSignal


class LearnerManager(Namespace):

    def __init__(self, socketio, namespace='/'):
        super().__init__(namespace)
        self.socketio = socketio
        self.learners = {}

    def spawn(self, room_id, config_filename, client_ip, user_agent):
        if room_id in self.learners:
            self.kill(room_id)
        self.learners[room_id] = Learner(self.socketio, room_id, config_filename, client_ip, user_agent)
        self.learners[room_id].initialize()

    def kill(self, room_id):
        if room_id in self.learners:
            del(self.learners[room_id])

    def on_log(self, data):
        room_id = request.sid
        if room_id in self.learners:
            print('[{}] {}'.format(self.learners[room_id].logger.log_folder, data))

    def on_spawn_learner(self, config_filename):
        room_id = request.sid
        full_config_filename = os.path.join(CONFIG_FOLDER, config_filename)
        client_ip = request.remote_addr
        user_agent = request.user_agent
        self.spawn(room_id, full_config_filename, client_ip, user_agent)

    def on_pad_ready(self, pad_ready_state):
        room_id = request.sid
        if room_id in self.learners:
            if pad_ready_state:
                self.learners[room_id].is_pad_ready = True
            else:
                self.learners[room_id].ask_pad_ready()

    def on_pad_clean(self, pad_clean_state):
        room_id = request.sid
        if room_id in self.learners:
            if pad_clean_state:
                self.learners[room_id].is_pad_clean = True
            else:
                self.learners[room_id].ask_pad_clean()

    def on_reset(self):
        room_id = request.sid
        if room_id in self.learners:
            config_filename = self.learners[room_id].config_filename
            client_ip = request.remote_addr
            user_agent = request.user_agent
            self.spawn(room_id, config_filename, client_ip, user_agent)

    def on_feedback_info(self, feedback_info):
        room_id = request.sid
        if room_id in self.learners:
            self.learners[room_id].step(feedback_info)


class Learner(object):

    def __init__(self, socketio, room_id, config_filename, client_ip, user_agent):
        self.socketio = socketio
        self.room_id = room_id
        self.config_filename = config_filename
        self.client_ip = client_ip
        self.user_agent = user_agent

    def initialize(self):
        print('[{}] Starting learner from {}'.format(self.room_id, self.config_filename))
        ##  read config
        self.config = read_config(self.config_filename)
        self.code_manager = CodeManager(self.config['code'])
        ## init a Logger
        self.logger = Logger()
        self.logger.log_new_connnection(self.client_ip, self.user_agent, self.room_id, self.config_filename, self.config)
        ## make sure pad is loaded
        self.init_pad()
        ## initialize the algortihm
        self.init_learner()
        ## make sure all element are correctly displayed
        self.classifier_last_solved = None
        self.n_iteration_at_last_solved = 0
        self.clean_pad()
        self.update_iteration(new_iteration_value=0)
        self.update_code(apply_pause=False)
        self.update_pad()
        self.update_flash_pattern()

    def init_pad(self):
        self.is_pad_ready = False
        # send client message to init pad
        pad_config = self.config['pad']
        self.socketio.emit('init_pad', pad_config, room=self.room_id)
        # ask and wait for confirmation that pad is ready
        self.ask_pad_ready()
        while not self.is_pad_ready:
            time.sleep(0.1)

    def ask_pad_ready(self):
        self.socketio.emit('is_pad_ready', room=self.room_id)

    def clean_pad(self):
        self.is_pad_clean = False
        # send client message to init pad
        self.socketio.emit('clean_pad', room=self.room_id)
        # ask and wait for confirmation that pad is ready
        self.ask_pad_clean()
        while not self.is_pad_clean:
            time.sleep(0.1)

    def ask_pad_clean(self):
        self.socketio.emit('is_pad_clean', room=self.room_id)

    def init_learner(self):
        learner_config = self.config['learner']
        if learner_config['type'] == 'discrete':
            self.learner = DiscreteLearner(
                learner_config['n_hypothesis'],
                learner_config['known_symbols'])
        elif learner_config['type'] == 'continuous':
            self.learner = ContinuousLearner(
                learner_config['n_hypothesis'],
                proba_decision_threshold=0.95,
                proba_assigned_to_label_valid=0.95)
            # only used for audi level but we will init it here anyway
            self.audio_transformer = AudioVaultSignal()
        else:
            raise Exception('Type of learner not defined in config file or not handled.')

    def step(self, feedback_info):
        if self.code_manager.is_code_decoded():
            raise Exception('Should never get there')
        else:
            self.update_iteration(self.n_iteration + 1)

            self.update_learner(feedback_info)

            if self.learner.is_inconsistent():
                self.socketio.emit('check', 'inconsistent', room=self.room_id)

            if self.learner.is_solved():
                # get the code info
                self.update_code()
                # prepare learner for next digit
                self.prepare_learner_for_next_digit()

            self.update_pad()

            if self.code_manager.is_code_decoded():
                if self.code_manager.is_check_procedure_required():
                    if self.code_manager.is_code_valid():
                        self.socketio.emit('check', 'valid', room=self.room_id)
                    else:
                        self.socketio.emit('check', 'invalid', room=self.room_id)
                else:
                    self.socketio.emit('no_check', room=self.room_id)
            else:
                self.update_flash_pattern()

    def update_iteration(self, new_iteration_value):
        self.n_iteration = new_iteration_value
        self.socketio.emit('n_iteration', self.n_iteration, room=self.room_id)

    def update_flash_pattern(self):
        self.socketio.emit(
            'update_flash',
            self.learner.get_next_flash_pattern(planning_method='even_uncertainty'),
            room=self.room_id)

    def update_learner(self, feedback_info):

        displayed_flash_patterns = feedback_info['flash']

        learner_config = self.config['learner']
        if learner_config['type'] == 'discrete':
            feedback_symbol = feedback_info['symbol']
            self.learner.update(displayed_flash_patterns, feedback_symbol)

        elif learner_config['type'] == 'continuous':

            if 'signal' in feedback_info:
                feedback_signal = feedback_info['signal']
                self.learner.update(displayed_flash_patterns, feedback_signal)

            elif 'mp3' in feedback_info:
                mp3_file = self.logger.save_mp3_to_file(feedback_info['mp3'])

                print('Received {} from user'.format(mp3_file))

                self.audio_transformer.add_feedback_mp3(mp3_file)
                feedback_signals, _ = self.audio_transformer.get_feedback_signals()

                self.learner.signal_history = feedback_signals[:-1]
                self.learner.update(displayed_flash_patterns, feedback_signals[-1])

            else:
                raise Exception('Not enough info to process in feedback_info.')


    def prepare_learner_for_next_digit(self):

        learner_config = self.config['learner']
        if learner_config['type'] == 'discrete':
            # if required, update known symbols with acquired ones
            if learner_config['accumulate_known_symbols_between_numbers']:
                solution_index = self.learner.get_solution_index()
                learner_config['known_symbols'] = self.learner.compute_symbols_belief_for_hypothesis(solution_index)
            # restart a new learner (with the original or new symbols set if updated above)
            self.init_learner()

        elif learner_config['type'] == 'continuous':
            if learner_config['accumulate_info_between_numbers']:
                solution_index = self.learner.get_solution_index()
                self.learner.propagate_labels_from_hypothesis(solution_index)
                # if we accumulate the info, we change this variable that is used to update the pad with learned information up to the current iteration
                self.classifier_last_solved = self.learner.hypothesis_classifier_infos[solution_index]['clf']
                self.n_iteration_at_last_solved = self.n_iteration
            else:
                # spawn a new learner from scratch
                self.init_learner()
        else:
            raise Exception('Learner of type {} not handled'. format(learner_config['type']))


    def update_code(self, apply_pause=True):
        # if new digit found
        if self.learner.is_solved():
            solution_index = self.learner.get_solution_index()
            self.code_manager.add_new_digit(solution_index)

        update_code_info = {}
        update_code_info['code_json'] = self.code_manager.code_json
        update_code_info['apply_pause'] = apply_pause

        self.socketio.emit('update_code', update_code_info, room=self.room_id)


    def update_pad(self):
        update_pad_info = {}

        pad_config = self.config['pad']
        if pad_config['show_learning_progress']:

            # those are constants and should be defined outside this scope but we prefer to define them here as they are only relevant here
            MEANING_TO_COLOR = {}
            MEANING_TO_COLOR[True] = 'flash'
            MEANING_TO_COLOR[False] = 'noflash'

            learner_config = self.config['learner']
            if learner_config['type'] == 'discrete':
                known_symbols = learner_config['known_symbols']

                button_color = ['neutral' for _ in range(pad_config['n_pad'])]
                for button_number, button_meaning in known_symbols.items():
                    button_color[int(button_number)] = MEANING_TO_COLOR[button_meaning]

                update_pad_info['button_color'] = button_color

            elif learner_config['type'] == 'continuous':
                # as many point as iteration so far
                signal_color = ['neutral' for _ in range(self.n_iteration)]
                # but only the one that have already been identified are colored
                for i in range(0, self.n_iteration_at_last_solved):
                    # labels have been propagated so up to self.n_iteration_at_last_solved iteration all labels are the same
                    label_for_ith_point = self.learner.hypothesis_labels[0][i]
                    signal_color[i] = MEANING_TO_COLOR[label_for_ith_point]

                update_pad_info['signal_color'] = signal_color

                ## if classifier solved, plot it, save it and send it
                if self.classifier_last_solved:
                    classifier_map = classifier_tools.generate_map_from_classifier(self.classifier_last_solved)

                    map_filename = self.logger.save_classifier_map_to_file(classifier_map)

                    # read image and convert it to a format I can send to the webpage
                    with open(map_filename, 'rb') as f:
                        map_image_base64 = base64.b64encode(f.read()).decode()
                    classifier_map_for_web = 'data:image/png;base64,{}'.format(map_image_base64)

                    update_pad_info['classifier_map'] = classifier_map_for_web

                    # we put classifier_last_solved back to None to not recompute and send again each iteration, but each time we update it
                    self.classifier_last_solved = None

        ## we send it everytime even if empty, just to be able to sync server and client in term of UI
        self.socketio.emit('update_pad', update_pad_info, room=self.room_id)


class CodeManager(object):

    def __init__(self, code_config):
        self.config =  code_config
        self.reset()

    def reset(self):
        self.decoded_code = [None for _ in self.secret_code]
        self.ongoing_digit_index = 0

    def is_check_procedure_required(self):
        return self.config['check_code']

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
    def code_json(self):
        code_json = []
        ongoing_not_set = True

        for digit in self.decoded_code:
            digit_json = {
                'found': False,
                'ongoing': False,
                'text': ''
            }

            if digit is None:
                if ongoing_not_set:
                    digit_json['ongoing'] = True
                    ongoing_not_set = False
            else:
                digit_json['found'] = True
                if self.config['show_code']:
                    digit_json['text'] = str(digit)
                else:
                    digit_json['text'] = '#'

            code_json.append(digit_json)

        return code_json
