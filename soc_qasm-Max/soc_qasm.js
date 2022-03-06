const path = require('path');
const Max = require('max-api');
const { io } = require("socket.io-client");
var dest; // destination address of the socket.io server (soc_qasm.py), if on the same machine it should be "http://127.0.0.1:5000"
var url = "http://127.0.0.1"; // destination ip of the socket.io server (soc_qasm.py), defaults to 
var port; // destination port of the socket.io server (soc_qasm.py)

// This will be printed directly to the Max console
Max.post('SOC-Qasm');
Max.post('OCH 2022');
// Max.post('SOC-Qasm [v1.0] is starting...');

if (process.argv[2]) {
	dest = process.argv[2];
} else {
	dest = "http://127.0.0.1:5000"; // default
}

function makedest(){
	if (port) {
		dest = url+":"+port;
	} else {
		dest = url;
	}
}

var socket = io(dest);

// Use the 'addHandler' function to register a function for a particular message
Max.addHandler("port", (number) => {	
	if (typeof number !="number") {
		Max.post("port needs to be a number", Max.POST_LEVELS.ERROR)
		return;
	}
	port = number;
	makedest();
	socket = io(dest);
	Max.post(`changed destination to ${dest}`);
});
Max.addHandler("url", (address) => {	
	if (typeof address !="string") {
		Max.post("url needs to be a string", Max.POST_LEVELS.ERROR)
		return;
	}
	if (address.substring(0, 4) != "http") {
		Max.post("url needs to start with either http:// or https://", Max.POST_LEVELS.ERROR)
		return;	
	}
	url = address;
	makedest();
	socket = io(dest);
	Max.post(`changed destination to ${dest}`);
});

socket.on("connect", () => {
  Max.post("soc_qasm connected to server");
  console.log(socket.id); // x8WIv7-mJelg7on_ALbx
});
socket.on("disconnect", () => {
  Max.post("soc_qasm disconnected from server");
  console.log(socket.id); // undefined
});
socket.on("response", (data) => {
  // if (data[0]=="counts") {Max.post("counts: "+data[1]);}
  Max.outlet(data);
  console.log(socket.id); // undefined
});

// Use the 'outlet' function to send messages out of node.script's outlet
Max.addHandler("send", (qasm, shots, backend) => {
	Max.outlet("info","sending qasm code...");
	if (backend) {
		if (typeof shots !="number") {
			Max.post("shots need to be a number, and greater than zero", Max.POST_LEVELS.ERROR)
			return;
		}
		socket.emit("QuTune", qasm, shots, backend);	
	} else if (shots) {
		if (typeof shots !="number") {
			Max.post("shots need to be a number, and greater than zero", Max.POST_LEVELS.ERROR)
			return;
		}
		socket.emit("QuTune", qasm, shots);	
	} else {
		socket.emit("QuTune", qasm);	
	}
});
