import time

import socketio

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

@sio.on('response')
def on_response(msg):
    print('received {} at {}'.format(msg, time.time()))
    sio.emit('receive', msg)

sio.connect('http://localhost:5000')

message = {}
message['data'] = 'foo'

sio.emit('receive', message)

sio.wait()



# @sio.on('my message')
# def on_message(data):
#     print('message received with ', data)
#     # sio.emit('my response', {'response': 'my response'})
