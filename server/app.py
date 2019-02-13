import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import time

from flask import Flask, render_template
from flask_socketio import SocketIO, emit


client_files=os.path.join(HERE_PATH, '../client/dist')
client_files=os.path.normpath(client_files)

print(client_files)

app = Flask(__name__, static_folder=client_files, template_folder=client_files, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_from_directory('', path)

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# @socketio.on('receive')
# def handle_message(data):
#     print('received {} at {}'.format(data, time.time()))
#     time.sleep(1)
#     response = {}
#     response['message'] = 'Count is {}'.format(data['cnt'])
#     response['cnt'] = data['cnt']
#     emit('response', response)


@socketio.on('emit_key')
def handle_it(data):
    print('##### KEY: {}'.format(data))

@socketio.on('emit_click')
def handle_it(data):
    print('##### CLICK: {}'.format(data))

if __name__ == '__main__':
    socketio.run(app)
