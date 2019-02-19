import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import numpy as np
import random
import string

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

client_files=os.path.join(HERE_PATH, '../client/dist')
client_files=os.path.normpath(client_files)

app = Flask(__name__, static_folder=client_files, template_folder=client_files, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)


from tinydb import TinyDB, Query, where
from tinyrecord import transaction

database = TinyDB('db.json').table('database')
database.purge()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_from_directory('', path)

@socketio.on('connect')
def on_connect():

    with transaction(database) as tr:
        join_room(request.sid)
        tr.insert({'room': request.sid})

    grid = [
        [{}, {"index": "3", "ref": "3", "message": "Hello"}, {"index": "4", "ref": "4"}, {}]
    ]

    emit('grid', {"grid": grid})

    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    with transaction(database) as tr:
        join_room(request.sid)
        tr.remove(where('room') == request.sid)

    print('Client disconnected')

@socketio.on('key')
def on_key(data):
    print('##### KEY: {}'.format(data))

@socketio.on('click')
def on_click(data):
    print(request.sid)
    print('##### CLICK: {}'.format(data))



if __name__ == '__main__':

    import eventlet

    ## from https://github.com/miguelgrinberg/python-socketio/issues/16
    def bg_emit():

        for items in database:

            room_name = items['room']

            grid = [
                [{}, {"index": "3", "ref": "3", "message": random.choice(string.ascii_letters)}, {"index": "4", "ref": "4", "message": str(random.randint(0, 9))}, {}]
            ]

            socketio.emit('grid', {"grid": grid}, room=room_name)

            socketio.emit('newnumber', {"number": np.random.rand()}, room=room_name)


    def listen():
        while True:
            bg_emit()
            eventlet.sleep(1)

    eventlet.monkey_patch(time=True)
    eventlet.spawn(listen)

    socketio.run(app)
