# SOC-Qasm
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6342383.svg)](https://doi.org/10.5281/zenodo.6342383)

A spinoff of [OSC-Qasm](https://github.com/iccmr-quantum/OSC-Qasm/). A simple Socket.io Python interface for executing Qasm code.

Control your soc_qasm.py module directly from the [web browser](https://quantumland-art.github.io/SOC-Qasm/).

## Installation
Before starting, make sure you have [Python](https://www.python.org/) 3.7+ in your system.
- when using the installer on windows make sure to select the option `Add Python X to PATH`

In order to try our Max patches, make sure you also have [Max](http://cycling74.com) installed, and [_The QAC Toolkit_](http://quantumland.art/qac) Max package available.

Clone or [download](https://github.com/iccmr-quantum/SOC-Qasm/archive/refs/heads/main.zip) and unzip this repo.

Open the Terminal (Mac) or Command Prompt (Windows) and navigate to the folder  where you saved the repo.
- see here a refresher on how to navigate using the terminal [[1](https://computers.tutsplus.com/tutorials/navigating-the-terminal-a-gentle-introduction--mac-3855)][[2](https://www.macworld.com/article/221277/command-line-navigating-files-folders-mac-terminal.html)]

Create a python virtual environment
- on the terminal, type: `python3 -m venv SOCQasm`
- depending on your system, you may simply use: `python -m venv SOCQasm`

Enter your new python virtual environment
- on mac: `source SOCQasm/bin/activate`
- on windows: `SOCQasm\Scripts\activate`

At the start of your terminal prompt, it should show `(SOCQasm)`, indicating that you're in your new virtual environment.

Update pip and setuptools
- `pip install --upgrade pip setuptools`
- Note: if for some reason you don't have pip, please [install it](https://phoenixnap.com/kb/install-pip-windows)

Install qiskit and python-osc
- `pip install qiskit python-socketio eventlet`

## Running

First, open a Terminal (Mac) or Command Prompt (Windows) and start you python environment.

Then run the python module: `python soc_qasm.py`
Wait until the program outputs the following lines:
```console
================================================
 SOC_QASM by OCH @ QuTune (v1.x)
 https://iccmr-quantum.github.io               
================================================
(xxxxx) wsgi starting up on http://0.0.0.0:PPPP
```
Now you can open the [soc_qasm.maxpat](soc_qasm-Max/soc_qasm.maxpat) in Max 8 and start sending messages with QuantumCircuits in Qasm, to the SOC-Qasm python module. Note: the first time you open [soc_qasm.maxpat](soc_qasm-Max/soc_qasm.maxpat) you might need to install the nodejs dependencies by clicking the `script npm install` message box on the right side. Use the `start/stop client` toggle on the left side to enable the node.script object before sending any qasm code.

You can also experiment interacting with your soc_qasm.py instance using a web browser. Open [this page](https://quantumland-art.github.io/SOC-Qasm/) for an example. You will notice that, independently of where this page is being hosted, it can still connect with your local soc_qasm.py. The source code for this page can be found in [docs/index.html](docs/index.html).

When you're done working with soc_qasm.py you can leave the virtual environment with
- on mac & windows: `deactivate`

### Additional arguments
You can also set some additional arguments and flags in front of `python soc_qasm.py`:

```console
usage: soc_qasm.py [-h] [--token TOKEN] [--hub HUB] [--group GROUP]
                   [--project PROJECT]
                   [port]

positional arguments:
  port       The port where the soc_qasm.py Server will listen for
                     incoming messages. Default port is 5000

optional arguments:
  -h, --help         show this help message and exit
  --token TOKEN      If you want to run circuits on real quantum hardware, you
                     need to provide your IBMQ token (see https://quantum-
                     computing.ibm.com/account)
  --hub HUB          If you want to run circuits on real quantum hardware, you
                     need to provide your IBMQ Hub
  --group GROUP      If you want to run circuits on real quantum hardware, you
                     need to provide your IBMQ Group
  --project PROJECT  If you want to run circuits on real quantum hardware, you
                     need to provide your IBMQ Project
```

The [soc_qasm.maxpat](soc_qasm-Max/soc_qasm.maxpat) patch also allows some customization using positional arguments. Make sure to check out the `p More-options` subpatch to learn more!

### Note

In order to access your soc_qasm.py instance from outside your local area network, you might need to either open the corresponding ports on your router (port forwarding), or use a vpn service like hamachi.
<!-- ![soc_qasm-help](./soc_qasm-help.png) -->




## Feedback and Getting help
Please open a [new issue](https://github.com/iccmr-quantum/SOC-Qasm/issues/new).

Also, please consider learning more about Max [here](https://cycling74.com/get-started), and Qiskit [here](https://qiskit.org/learn), as well as explore the [Intro to Quantum Computer Music](https://github.com/iccmr-quantum/Intro-to-Quantum-Computer-Music) Tutorial (video recording [here](https://youtu.be/6UrNguY8zGY?t=1143)) and the other projects in [QuTune's Github](https://github.com/iccmr-quantum).

## Acknowledgements
SOC-Qasm is a spinoff of [OSC-Qasm](https://github.com/iccmr-quantum/OSC-Qasm/) which is inspired by Jack Woehr's [Qisjob project](https://zenodo.org/record/4554481), and the och.qisjob [object](https://www.quantumland.art/phd).

This repo was created by Omar Costa Hamido as part of the [QuTune Project](https://iccmr-quantum.github.io/).
