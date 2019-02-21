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

# say the server where to serve the static files
server_folder=os.path.normpath(os.path.join(HERE_PATH, '../client/dist'))
app = Flask(__name__, static_folder=server_folder, template_folder=server_folder, static_url_path='')

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

# we initialise the learner and pass the instance of socketio
import learner_tools
learner_manager = learner_tools.LearnerManager(socketio)

# create and add the handlers specific to our learning task
learner_namespace = learner_tools.LearnerNamespace('/', learner_manager)
socketio.on_namespace(learner_namespace)


# when opening the root, we server index.html
@app.route('/')
def index():
    return render_template('index.html')

# if the page need to load files, this allow the server to server them for all urls
@app.route('/<path:path>')
def serve_static(path):
    return app.send_from_directory('', path)

# on connect, join room, update database, start a learner for this room
@socketio.on('connect')
def on_connect():
    room_id = request.sid
    print('Client {} connected'.format(room_id))
    join_room(room_id)
    with transaction(database) as tr:
        tr.insert({'room_id': room_id})
    learner_manager.init(room_id)

# on disconnect, leave room, update database, delete the learner for this room
@socketio.on('disconnect')
def on_disconnect():
    room_id = request.sid
    print('Client {} disconnected'.format(room_id))
    leave_room(room_id)
    with transaction(database) as tr:
        tr.remove(where('room_id') == room_id)
    learner_manager.delete(room_id)


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
