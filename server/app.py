import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


# we initialize the web server
from flask import Flask, render_template, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room

from tools import APP_NAME, SERVE_FOLDER, CONFIG_FOLDER, get_configs
app = Flask(APP_NAME, static_folder=SERVE_FOLDER, template_folder=SERVE_FOLDER, static_url_path='')

socketio = SocketIO(app)

# we initialise the learner and pass the instance of socketio
from learner_tools import LearnerManager
learner_manager = LearnerManager(socketio)
socketio.on_namespace(learner_manager)


# when opening the root url, we server index.html that was compiled via npm in SERVE_FOLDER
@app.route('/')
def index():
    return render_template('index.html')

# if the page need to load files, this allow the server to server them for all urls
# @app.route('/<path:path>')
# def serve_static(path):
#     return app.send_from_directory('', path)


# on connect, join room, update database
@socketio.on('connect')
def on_connect():
    room_id = request.sid
    join_room(room_id)


# on disconnect, leave room, update database
# delete the learner for this room if created
@socketio.on('disconnect')
def on_disconnect():
    room_id = request.sid
    leave_room(room_id)
    learner_manager.kill(room_id)


@socketio.on('get_configs')
def on_get_configs():
    emit('set_configs', get_configs())


# if ran from gunicorn make log works
# from https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f
if __name__ != '__main__':
    import logging
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


# if ran using python app.py
if __name__ == '__main__':
    print('Flask is running in python')

    # import eventlet
    # import random
    #
    # def random_boolean():
    #     return random.choice([True, False])
    #
    # def random_text():
    #     return random.choice(['#', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    #
    # def random_pad_color():
    #     return random.choice(['flash', 'noflash', 'neutral'])
    #
    # ## from https://github.com/miguelgrinberg/python-socketio/issues/16
    # def background_emit():
    #     while True:
    #         pad_color = [random_pad_color() for _ in range(9)]
    #         socketio.emit('update_pad', pad_color)
    #         eventlet.sleep(1)
    #
    # eventlet.monkey_patch(time=True)
    # eventlet.spawn(background_emit)

    socketio.run(app, host='0.0.0.0', debug=False)
