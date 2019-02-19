import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

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


# adding openvault directory to path
import sys
openvault_path = os.path.join(HERE_PATH, '..', '..', 'openvault')
sys.path.append(openvault_path)

from discrete import DiscreteLearner

learners = {}
flash_patterns = {}

FLASH_COLORS = {}
FLASH_COLORS[True] = 'rgba(220, 0, 0, 0.5)'
FLASH_COLORS[False] = 'rgba(255, 255, 255, 1)'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_from_directory('', path)

@socketio.on('connect')
def on_connect():
    room_id = request.sid
    print('Client {} connected'.format(room_id))
    join_room(room_id)
    with transaction(database) as tr:
        tr.insert({'room_id': room_id})

    learners[room_id] = DiscreteLearner(4)

    display_grid = [
        [
            {"index": "n1", "message": "1"},
            {"index": "n2", "message": "2"},
            {"index": "n3", "message": "3"},
            {"index": "n4", "message": "4"}
        ]
    ]
    emit('grid', {"panel_index": "display", "grid": display_grid})


    code_grid = [
        [
            {"index": "c1", "message": "#", "fontSize": "100px"},
            {"index": "c2", "message": "#", "fontSize": "100px"},
            {"index": "c3", "message": "#", "fontSize": "100px"},
            {"index": "c4", "message": "", "fontSize": "100px"}
        ]
    ]
    emit('grid', {"panel_index": "code", "grid": code_grid})


    pad_grid = [
        [
            {"index": "p1", "message": ""},
            {"index": "p2", "message": ""},
            {"index": "p3", "message": ""},
            {"index": "p4", "message": ""}
        ]
    ]
    emit('grid', {"panel_index": "pad", "grid": pad_grid})

    emit('ready', {"panel_index": "display"})


def update_learner(room_id, feedback_symbol):
    print('##### Updating {} for {} with {}'.format(room_id, flash_patterns[room_id], feedback_symbol))
    learners[room_id].update(flash_patterns[room_id], feedback_symbol)

def send_flash_pattern(room_id):

    flash_patterns[room_id] = learners[room_id].get_next_flash_pattern()

    colors = [
        [
            FLASH_COLORS[flash_patterns[room_id][0]],
            FLASH_COLORS[flash_patterns[room_id][1]],
            FLASH_COLORS[flash_patterns[room_id][2]],
            FLASH_COLORS[flash_patterns[room_id][3]]
        ]
    ]

    socketio.emit('colors', {"panel_index": "display", "colors": colors}, room=room_id)

    # print(learners[room_id].is_inconsistent())
    # print(learners[room_id].is_solved())
    if learners[room_id].is_solved():
        print('###########')
        print('###########')
        solution_index = learners[room_id].get_solution_index()
        updated_known_symbols = learners[room_id].compute_symbols_belief_for_hypothesis(solution_index)
        reset_learner(room_id, updated_known_symbols)

        print(solution_index + 1)
        print(updated_known_symbols)
        print('###########')
        print('###########')

def reset_learner(room_id, updated_known_symbols):
    learners[room_id] = DiscreteLearner(4, updated_known_symbols)

@socketio.on('disconnect')
def on_disconnect():
    room_id = request.sid
    print('Client {} disconnected'.format(room_id))
    leave_room(room_id)
    with transaction(database) as tr:
        tr.remove(where('room_id') == room_id)
    del(learners[room_id])

@socketio.on('status')
def on_status(data):
    room_id = request.sid
    if data['status']:
        send_flash_pattern(room_id)
    else:
        eventlet.sleep(1)
        emit('ready', {"panel_index": "display"})

@socketio.on('key')
def on_key(data):
    room_id = request.sid
    print('##### KEY: {}'.format(data))
    update_learner(room_id, data['key'])
    send_flash_pattern(room_id)

@socketio.on('click')
def on_click(data):
    room_id = request.sid
    print('##### CLICK: {}'.format(data))
    update_learner(room_id, data['tile_index'])
    send_flash_pattern(room_id)


if __name__ == '__main__':

    import eventlet

    import numpy as np
    import random
    import string


    def random_hex_color():
        r = lambda: random.randint(0,255)
        return '#{:02x}{:02x}{:02x}'.format(r(), r(), r())

    ## from https://github.com/miguelgrinberg/python-socketio/issues/16
    def background_emit():

        for items in database:

            room_name = items['room']

            for panel_index in ["code", "pad"]:

                grid = [
                    [{}, {"index": "3", "message": random.choice(string.ascii_letters)}, {"index": "4", "message": str(random.randint(0, 9))}, {}]
                ]

                socketio.emit('grid', {"panel_index": panel_index, "grid": grid}, room=room_name)


            flash_pattern = learners[room_name].get_next_flash_pattern()

            print(room_name, flash_pattern)

            flash_colors = {}
            flash_colors[True] = 'red'
            flash_colors[False] = 'white'

            colors = [
                [
                    flash_colors[flash_pattern[0]],
                    flash_colors[flash_pattern[1]]
                ]
            ]

            socketio.emit('colors', {"panel_index": "display", "colors": colors}, room=room_name)



    def listen():
        while True:
            background_emit()
            eventlet.sleep(1)

    eventlet.monkey_patch(time=True)
    # eventlet.spawn(listen)

    socketio.run(app)
