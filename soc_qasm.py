# SOC-Qasm
# A simple Socket.io Python interface for executing Qasm code.
# Or a simple bridge to connect _The QAC Toolkit_ with real quantum hardware.
#
# Omar Costa Hamido (2022-03-06)
# https://github.com/iccmr-quantum/SOC-Qasm
#

# from pythonosc import dispatcher, osc_server, udp_client
from qiskit import *
from qiskit.test.mock import *
from qiskit.tools import job_monitor
import argparse
import sys
import socketio
import eventlet

sio = socketio.Server(async_mode='eventlet',cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

class FileLikeOutputOSC(object):
    ''' This class emulates a File-Like object
        with a "write()" method that can be used
        by print() and qiskit.tools.job_monitor()
        as an alternative output (replacing sys.stdout)
        to send messages through the OSC-Qasm client

        usage: print("foo", file=FileLikeOutputOSC())
        '''
    def __init__(self):
        pass

    def write(self, text):
        if text != f'\n' and text != "": # Skips end='\n'|'' argument messages
            print(text) # Print back to console
            # Send message body back to Max on info channel
            sio.emit('response', ['info', text[12:]], room=SID)
            # client.send_message("info", text[12:])

class FileLikeErrorOSC(object):
    ''' This class emulates a File-Like object
        with a "write()" method that can be used
        to pipe Qiskit error messages through
        the OSC-Qasm client

        usage: sys.stderr = FileLikeErrorOSC()
        '''
    def __init__(self):

        self.older="" # stderr 'memory'

    def write(self, text):
        if text != f'\n' and text != "": # Skips end='\n'|'' argument messages
            print(text) # Print back to console

            if text == ERR_SEP and self.older != ERR_SEP and self.older != "": # There is a line like ERR_SEP both at the begining and end of a qiskit error log!
                # Print the last entry before the ending ERR_SEP
                sio.emit('response', ['error', "error in osc_qasm.py: \n(...) "+self.older+"switch to python console to learn more"], room=SID)
                # client.send_message("error", "error in osc_qasm.py: \n(...) "+self.older+"switch to python console to learn more")

            elif "KeyboardInterrupt" in text:
                # When closing the program with Ctrl+c, There is a 'KeyboardInterrupt' error message.
                sio.emit('response', ['error', "osc_qasm.py has been terminated in the Python environment."], room=SID)
                # client.send_message("error", "osc_qasm.py has been terminated in the Python environment.")

            self.older=text # Update memory

def run_circuit(qc, shots, backend_name):
    print("SID3: ",SID)
    print("Running circuit on {}...".format(backend_name))
    sio.emit('response', ['info', "Running circuit on {}...".format(backend_name)], room=SID)
    # client.send_message("info", "Running circuit on {}...".format(backend_name) )

    flosc = FileLikeOutputOSC() # Use this only for job_monitor output

    if backend_name != 'qasm_simulator':
        if backend_name in ('FakeAlmaden', 'FakeArmonk', 'FakeAthens', 'FakeBelem', 'FakeBoeblingen', 'FakeBogota', 'FakeBrooklyn', 'FakeBurlington', 'FakeCambridge', 'FakeCambridgeAlternativeBasis', 'FakeCasablanca', 'FakeEssex', 'FakeGuadalupe', 'FakeJakarta', 'FakeJohannesburg', 'FakeLagos', 'FakeLima', 'FakeLondon', 'FakeManhattan', 'FakeManila', 'FakeMelbourne', 'FakeMontreal', 'FakeMumbai', 'FakeOurense', 'FakeParis', 'FakePoughkeepsie', 'FakeQuito', 'FakeRochester', 'FakeRome', 'FakeRueschlikon', 'FakeSantiago', 'FakeSingapore', 'FakeSydney', 'FakeTenerife', 'FakeTokyo', 'FakeToronto', 'FakeValencia', 'FakeVigo', 'FakeYorktown'):
            backend_name+='()'
            backend = eval(backend_name) # this is definitely a security hazard... use at your own risk!
                # a very interesting alternative is to use: backend = globals()[backend_name]
            available_qubits = backend.configuration().n_qubits
            requested_qubits = qc.num_qubits
            if requested_qubits > available_qubits: # verify if the qubit count is compatible with the selected backend
                sio.emit('response', ['error', "The circuit submitted is requesting {} qubits but the {} backend selected only has {} available qubits.".format(requested_qubits,backend_name[:-2],available_qubits)], room=SID)
                # client.send_message("error", "The circuit submitted is requesting {} qubits but the {} backend selected only has {} available qubits.".format(requested_qubits,backend_name[:-2],available_qubits) )
                print('The circuit submitted is requesting {} qubits but the {} backend selected only has {} available qubits.'.format(requested_qubits,backend_name[:-2],available_qubits))
                sys.exit()
            job = execute(qc, shots=shots, backend=backend)
            pass
        else: #we then must be naming a realdevice
            if not provider: #for which we definitely need credentials! D:
                sio.emit('response', ['error', "You need to start osc_qasm.py with the following arguments: --token (--hub, --group, --project)."], room=SID)
                # client.send_message("error", "You need to start osc_qasm.py with the following arguments: --token (--hub, --group, --project).")
                print('You need to start osc_qasm.py with the following arguments: --token (--hub, --group, --project).')
                sys.exit()
            backend = provider.get_backend(backend_name)
            job = execute(qc, shots=shots, backend=backend)
            job_monitor(job, output=flosc, line_discipline="") # 'flosc' (FileLikeOutputOSC) reroutes the output from stdout to the OSC client
    else:
        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, shots=shots, backend=backend)
    print("Done!")
    return job.result().get_counts()

def parse_qasm(*args):
    global qc
    print("args: ",args)
    print("args size: ", len(args))
    qc=QuantumCircuit().from_qasm_str(args[0])

    if len(args)>1:
        shots = args[1]
        pass
    else:
        shots=1024

    if len(args)>2:
        backend_name = args[2]
    else:
        backend_name='qasm_simulator'

    counts = run_circuit(qc, shots, backend_name)
    print("Sending result counts back to Max")
    sio.emit('response', ['info', 'Retrieving results from osc_qasm.py...'], room=SID)
    # client.send_message("info", "Retrieving results from osc_qasm.py..." )
    # list comprehension that converts a Dict into an
    # interleaved string list: [key1, value1, key2, value2...]
    sorted_counts = {}
    for key in sorted(counts):
        #print ("%s: %s" % (key, counts[key]) )
        sorted_counts[key]=counts[key]
    counts_list = [str(x) for z in zip(sorted_counts.keys(), sorted_counts.values()) for x in z]
    # and then into a string
    counts_list = " ".join(counts_list)
    sio.emit('response', ['counts', counts_list], room=SID)
    # client.send_message("counts", counts_list)

def main(PORT, TOKEN, HUB, GROUP, PROJECT):

    global client, provider, ERR_SEP
    ERR_SEP = '----------------------------------------' # For FileLikeErrorOSC() class
    provider=None

    if TOKEN:
        IBMQ.enable_account(TOKEN, 'https://auth.quantum-computing.ibm.com/api', HUB, GROUP, PROJECT)
        provider=IBMQ.get_provider(hub=HUB, group=GROUP, project=PROJECT)
        pass
    # if UDP_IP=="localhost":
    #     UDP_IP="127.0.0.1"
    #     pass

    #SOC server and reply
    @sio.event
    def connect(sid, environ):
        print('new connection: ', sid)

    @sio.event
    def QuTune(sid, *data):
        # print('message ', data)
        global SID
        SID = sid
        print("data size: ",len(data))
        # sio.emit('response', ['foobar', 'foobar2'], room=SID) # this is an example of how to respond
        parse_qasm(*data)

    @sio.event
    def disconnect(sid):
        print('disconnected from: ', sid)

    eventlet.wsgi.server(eventlet.listen(('', PORT)), app)
    # print("Server is now receiving messages on port {}".format(PORT))

    # #OSC server and client
    # callback = dispatcher.Dispatcher()
    # server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", RECEIVE_PORT), callback)
    # client = udp_client.SimpleUDPClient(UDP_IP, SEND_PORT)
    # client.send_message("info", "osc_qasm.py is now running")

    # callback.map("/QuTune", parse_qasm)
    # print("Server Receiving on {} port {}".format(server.server_address[0], server.server_address[1]))
    # print("Server Sending back on {} port {}".format(client._address,  client._port))
    # server.serve_forever()


if __name__ == '__main__':

    p = argparse.ArgumentParser()

    p.add_argument('port', type=int, nargs='?', default=5000, help='The port where the soc_qasm.py Server will listen for incoming messages. Default port is 5000')
    # p.add_argument('send_port', type=int, nargs='?', default=1417, help='The port that osc_qasm.py will use to send messages back to Max. Default port is 1417')
    # p.add_argument('ip', nargs='?', default='127.0.0.1', help='The IP address where the client (Max/MSP) is located. Default IP is 127.0.0.1 (localhost)')
    p.add_argument('--token', help='If you want to run circuits on real quantum hardware, you need to provide your IBMQ token (see https://quantum-computing.ibm.com/account)')
    p.add_argument('--hub', help='If you want to run circuits on real quantum hardware, you need to provide your IBMQ Hub')
    p.add_argument('--group', help='If you want to run circuits on real quantum hardware, you need to provide your IBMQ Group')
    p.add_argument('--project', help='If you want to run circuits on real quantum hardware, you need to provide your IBMQ Project')

    args = p.parse_args()

    # Route sys.stderr to OSC
    flerr = FileLikeErrorOSC()
    sys.stderr = flerr

    if args.token:
        if not args.hub or not args.group or not args.project:
            if not args.hub and not args.group and not args.project:
                args.hub='ibm-q'
                args.group='open'
                args.project='main'
                pass
            else:
                raise ValueError('You need to specify both --hub, --group, and --project arguments.')
                args.hub=None
                args.group=None
                args.project=None

    print('================================================')
    print(' SOC_QASM by OCH @ QuTune (v1.0) ')
    print(' https://iccmr-quantum.github.io               ')
    print('================================================')
    main(args.port, args.token, args.hub, args.group, args.project)
