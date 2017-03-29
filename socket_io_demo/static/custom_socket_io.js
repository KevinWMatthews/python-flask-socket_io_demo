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

$(function() {
    $('#fileupload').fileupload({
        dataType: 'json',       // Expect the server to return valid json.
        replaceFileInput: false,

        add: function (e, data) {
            // Remove upload button if it already exists.
            $('#upload_button').remove();
            // Add an 'upload' button.
            data.context = $('<button/ id="upload_button">').text('Upload')
                .appendTo("#fileupload_div")
                .click(function () {
                    // Replace button with unclickable text once the upload has been started.
                    console.log('Upload add: user clicked upload button.');
                    data.context = $('<p/>').text('Uploading...').replaceAll($(this));
                    data.submit();
                }
            );
        },

        submit: function (e, data) {
            //TODO check if the file exists.
            //TODO reject files with wrong extension?
            console.log('Upload submit: ' + data.originalFiles[0].name);
            $('#fileupload').prop('disabled', true);
            logStatus(status_log, 'Sending file to server: ' + data.originalFiles[0].name);
        },

        // The docs say that this generally does not hit because the error callback hits when
        // the server returns a valid HTTP response? But it seem to be hitting....
        //TODO if the wrong extension is selected, I don't know where to find the error message.
        fail: function (e, data) {
            console.log('Upload fail: ' + data.textStatus + ' ' + data.errorThrown);
            logError(status_log, 'Upload failed: ' + data.errorThrown);
        },

        // Not sure about the distinction between the error and fail callbacks,
        // but fail is giving a more descriptive errorThrown message.
        /* error: function (e, data) {
         *  console.log('Upload: ' + data.textStatus + ' ' + data.errorThrown);
         *  logStatus(status_log, 'Upload error: ' + data.errorThrown);
        }, */

        progressall: function (e, data) {
            // This increments the progress bar.
            var progress = parseInt(data.loaded / data.total * 100, 10);
            updateProgressBar('upload_bar', progress);
        },

        // This processes the firmware python view's response.
        done: function (e, data) {
            console.log('Upload finished!');

            json = data.jqXHR.responseJSON;     // Ok then.
            console.log(json);
            if (json.status_message === 'fail') {
                console.log('Upload failed: ', json.error_message);
                logError(status_log, 'Upload failed: ' + json.error_message);
                logError(status_log, 'Upgrade will not complete.');
                return;
            }
            else {
                logStatus(status_log, 'Upload finished!');
            }
        },
    });
});

function updateProgressBar(id, progress) {
    $('#' + id).css('width', progress + '%').attr('aria-valuenow', progress + '%');
}

function logStatus(log, message) {
    log.innerHTML +=
        "<div><span>" + message + "</span></div>";
}

function logError(log, message) {
    log.innerHTML +=
        "<div><span class='text-danger'>" + message + "</span></div>";
}
