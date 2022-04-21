from qiskit import *
import socketio
import sys

## variables
password='password'
qasm=None # to be defined
shots=1024
backend="qasm_simulator"

## creating QuantumCircuit and retrieving Qasm code
qc = QuantumCircuit( 5,5 )

for i in range( 5 ):
    qc.h( i )
    if i != 0:
        qc.cx( i-1, i )
    else:
        pass

qc.measure_all()

qasm=qc.qasm()

print(qasm)

## sending to SOC-Qasm SaaS
## https://python-socketio.readthedocs.io/en/latest/server.html
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def response(data):
    print('message received with ', data)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('https://soc-qasm.och.pw')
# maybe https://github.com/miguelgrinberg/python-socketio/blob/main/src/socketio/client.py#L79
# or https://github.com/miguelgrinberg/python-socketio/blob/main/src/socketio/client.py#L295
# on the browser it is this https://socket.io/docs/v4/client-options/#timeout
sio.emit('QuTune', (password, qasm, shots, backend))
sio.wait()
