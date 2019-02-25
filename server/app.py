import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


# we will keep a simple database of rooms used
# 1 room == 1 user
from tinydb import TinyDB, where
from tinyrecord import transaction

database = TinyDB('rooms.json')
database.purge()

# we initialize the web server
from flask import Flask, render_template, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room

from tools import SERVER_FOLDER
app = Flask(__name__, static_folder=SERVER_FOLDER, template_folder=SERVER_FOLDER, static_url_path='')

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

# we initialise the learner and pass the instance of socketio
from learner_tools import LearnerManager
learner_manager = LearnerManager(socketio)
socketio.on_namespace(learner_manager)

import config_tools

# when opening the root, we server index.html
@app.route('/')
def index():
    return render_template('index.html')

# if the page need to load files, this allow the server to server them for all urls
@app.route('/<path:path>')
def serve_static(path):
    return app.send_from_directory('', path)

# on connect, join room, update database
@socketio.on('connect')
def on_connect():
    room_id = request.sid
    join_room(room_id)
    with transaction(database) as tr:
        tr.insert({'room_id': room_id})
    print('{} clients connected'.format(len(database.all())))

# on disconnect, leave room, update database
# delete the learner for this room if created
@socketio.on('disconnect')
def on_disconnect():
    room_id = request.sid
    leave_room(room_id)
    with transaction(database) as tr:
        tr.remove(where('room_id') == room_id)
    learner_manager.kill(room_id)
    print('{} clients connected'.format(len(database.all())))

@socketio.on('get_configs')
def on_get_configs():
    emit('set_configs', config_tools.get_configs())

@socketio.on('spawn_learner')
def on_spawn_learner(config_filename):
    room_id = request.sid
    full_config_file = os.path.join(
        config_tools.CONFIG_FOLDER,
        config_filename)
    learner_manager.spawn(room_id, full_config_file)


if __name__ == '__main__':

    # import eventlet
    # import numpy as np
    #
    # ## from https://github.com/miguelgrinberg/python-socketio/issues/16
    # def background_emit():
    #     while True:
    #         for items in database:
    #             room_name = items['room_id']
    #             socketio.emit('watchdog', np.random.rand(), room=room_name)
    #         eventlet.sleep(1)
    #
    # eventlet.monkey_patch(time=True)
    # eventlet.spawn(background_emit)

    socketio.run(app)
