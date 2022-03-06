# soc-server.py

import socketio
import eventlet

sio = socketio.Server(async_mode='eventlet')

app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def QuTune(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

# eventlet.wsgi.server(eventlet.listen(('', 5000)), app)