var UI = {}
var game_state;
var socket;
var my_id;
var html_styles
var messageFadeTime

function show_message(message) {
  const new_message = document.createElement("span");
  new_message.textContent = message;
  new_message.classList.add('message');
  UI.messages.append(new_message);
  setTimeout(
    function() {new_message.remove()},
    messageFadeTime*1000
  )
}

function update_player_list() {
  UI.player_list.replaceChildren();
  const player_ids = Object.keys(game_state.players);
  for (let player_id of player_ids) {
    let player_name = game_state.players[player_id].name;
    if (player_id == my_id) {
      player_name = player_name + " (me)";
    }
    const player_line = document.createElement("p");
    player_line.textContent = player_name;
    player_list.append(player_line);
  }

}

document.addEventListener("DOMContentLoaded", function() {
  UI.canvas = document.getElementById("main_canvas");
  UI.canvas.width = 400;
  UI.canvas.height = 200;
  UI.ctx = UI.canvas.getContext('2d');
  UI.start_game_button = document.getElementById('start_game_button');
  UI.player_list = document.getElementById('player_list');
  UI.player_name_input = document.getElementById('player_name_input');
  UI.chat_input = document.getElementById('chat_input');
  UI.messages = document.getElementById('messages');

  htmlStyles = window.getComputedStyle(document.documentElement);
  let messageFadeTimeRaw = htmlStyles.getPropertyValue('--message-fade-time');
  let match = messageFadeTimeRaw.match(/([0-9]*\.?[0-9]+)\s*s/);
  messageFadeTime = match[1];

  UI.start_game_button.onclick = function (event) {
    window.location.href = '/game'
  };
  UI.chat_input.addEventListener('keydown', function(event) {
    // Check if the pressed key is "Enter"
    if (event.key === 'Enter') {
      socket.emit('chat', {data: UI.chat_input.value});
      UI.chat_input.value = '';
    }
  });
  UI.player_name_input.addEventListener('keydown', function(event) {
    // Check if the pressed key is "Enter"
    let new_name = UI.player_name_input.value;
    if (event.key === 'Enter' && new_name.length > 0) {
      socket.emit('rename', {data: new_name});
      UI.chat_input.value = '';
    }
  });

  // var socket = io();  // Uses html server address/port
  socket = io({
    transports: ['polling'],
    reconnection: true,
    reconnectionAttempts: 10,
    reconnectionDelay: 1000
  });

  socket.on('update_game_state', function(msg) {
    game_state = msg['data'];
    comment = msg['comment'];
    show_message(comment);
    update_player_list();
  });
  socket.on('message', function(msg) {
    console.log('displaying message:', msg.data)
    show_message(msg.data);
  });

  socket.on('your_id', function(msg) {
    my_id = msg.data;
  });

  socket.on('connect', function(msg) {
  });

});
