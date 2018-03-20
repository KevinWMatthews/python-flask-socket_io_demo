// Reference socket.io-client at:
// https://github.com/socketio/socket.io-client

var status_log = document.getElementById('status_log');

var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    message = 'SocketIO connected';
    console.log(message);
    logStatus(status_log, message);
});

socket.on('disconnect', function() {
    message = 'SocketIO disconnected';
    console.log(message);
    logStatus(status_log, message);
});

socket.on('custom event', function(message) {
    output = 'Javascript received a custom event: ';
    console.log(output + message);
    logStatus(status_log, output + message);
});

socket.on('message', function(message) {
    output = 'Javascript received a message: ';
    console.log(output + message);
    logStatus(status_log, output + message);
});

function emitString() {
    event_type = 'javascript_emit'
    message = "Javascript SocketIO emitted a message.";
    console.log(message);
    // emit(event, message)
    // emit() allows you to send custom event types
    socket.emit(event_type, message);   // The python and javascript must agree on the message content
    logStatus(status_log, message);
}

function sendString() {
    message = "Javascript SocketIO sent a message.";
    console.log(message);
    // send(message)
    // send() allows you to send messages with the 'message' event
    socket.send(message);   // There is more to it than this...
    logStatus(status_log, message);
}

function emitJson() {
    event_type = 'javascript_json';
    message = "Javascript SocketIO emitted JSON.";
    json = {data: message}
    console.log(message);
    console.log(json);
    socket.emit(event_type, json);
    logStatus(status_log, message);
}

// It gets complicated to do this because send() always triggers the 'message' event in python,
// which would now responsible for parsing both strings and JSON (and anything else we ever send).
// function sendJson() {
// }

// The javascript emits the event and the python does nothing.
function emitUnhandledEvent() {
    event_type = 'python_does_not_handle';
    message = 'Javascript SocketIO emitted an event that python does not handle.';
    console.log(message);
    socket.emit(event_type, message);
    logStatus(status_log, message);
}

function requestEmitCustomEvent() {
    event_type = 'javascript_request_emit_custom_event';
    message = "Javascript SocketIO is requesting that Python emit a 'Custom Event'";
    console.log(message);
    socket.emit(event_type, message);
    logStatus(status_log, message);
}

function requestSend() {
    event_type = 'javascript_request_send';
    message = 'Javascript SocketIO is requesting that Python send a message';
    console.log(message);
    socket.emit(event_type, message);
    logStatus(status_log, message);
}

function requestUnhandleEvent() {
    event_type = 'javascript_request_unhandled';
    message = 'Javascript SocketIO is requesting that Python emit an event that Javascript does not handle';
    console.log(message);
    socket.emit(event_type, message);
    logStatus(status_log, message);
}

function logStatus(log, message) {
    log.innerHTML +=
        "<div><span>" + message + "</span></div>";
}

function logError(log, message) {
    log.innerHTML +=
        "<div><span class='text-danger'>" + message + "</span></div>";
}
