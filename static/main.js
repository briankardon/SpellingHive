var canvas;
var ctx;
var log;
var emit_data;
var emit_form;
var broadcast_form;


document.addEventListener("DOMContentLoaded", function() {
  canvas = document.getElementById("main_canvas");
  canvas.width = '100%';
  canvas.height = '50%';
  ctx = canvas.getContext('2d');
  log = document.getElementById('log');
  emit_data = document.getElementById('emit_data');
  emit_form = document.getElementById('emit');
  broadcast_form = document.getElementById('broadcast');

  var socket = io();  // Uses html server address/port
  socket.on('my response', function(msg) {
    console.log('got response!')
    const logEntry = document.createElement("p");
    logEntry.textContent = 'Received: ' + msg.data;
    log.append(logEntry);
  });
  emit_form.addEventListener('submit', (event) => {
    event.preventDefault();
    console.log('sending message!')
    socket.emit('my event', {data: emit_data.value});
    return false;
  });
  // broadcast_form.submit(function(event) {
  //     socket.emit('my broadcast event', {data: document.getElementById('broadcast_data').val()});
  //     return false;
  // });
});
