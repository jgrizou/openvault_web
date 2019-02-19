import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import numpy as np
import random
import string

from flask import Flask, render_template, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room

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
    print('Client {} connected'.format(request.sid))
    join_room(request.sid)
    with transaction(database) as tr:
        tr.insert({'room': request.sid})

@socketio.on('disconnect')
def on_disconnect():
    print('Client {} disconnected'.format(request.sid))
    leave_room(request.sid)
    with transaction(database) as tr:
        tr.remove(where('room') == request.sid)

@socketio.on('key')
def on_key(data):
    print('##### KEY: {}'.format(data))

@socketio.on('click')
def on_click(data):
    print('##### CLICK: {}'.format(data))



if __name__ == '__main__':

    import eventlet


    def random_hex_color():
        r = lambda: random.randint(0,255)
        return '#{:02x}{:02x}{:02x}'.format(r(), r(), r())

    ## from https://github.com/miguelgrinberg/python-socketio/issues/16
    def background_emit():

        for items in database:

            room_name = items['room']

            for panel_index in ["display", "code", "pad"]:

                grid = [
                    [{}, {"index": "3", "ref": "3", "message": random.choice(string.ascii_letters)}, {"index": "4", "ref": "4", "message": str(random.randint(0, 9))}, {}]
                ]

                socketio.emit('grid', {"panel_index": panel_index, "grid": grid}, room=room_name)

            colors = [
                [{}, random_hex_color(), random_hex_color(), {}]
            ]

            socketio.emit('colors', {"panel_index": "pad", "colors": colors}, room=room_name)



    def listen():
        while True:
            background_emit()
            eventlet.sleep(1)

    eventlet.monkey_patch(time=True)
    eventlet.spawn(listen)

    socketio.run(app)
