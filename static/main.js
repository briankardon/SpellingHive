var UI = {}
var game_state;
var socket;
var my_id;

function log_msg(...msg) {
  const logEntry = document.createElement("p");
  logEntry.textContent = msg;
  UI.log.append(logEntry);
}

function update_game_state_display() {
  if (!game_state) {
    return;
  }
  update_letter_display();
  update_word_lists();
}

function update_word_lists() {
  if (!game_state) {
    return;
  }
  console.log(game_state)
  UI.word_lists_container.replaceChildren();
  const player_ids = Object.keys(game_state.players);
  for (let player_id of player_ids) {
    let player_name = game_state.players[player_id].name;
    if (player_id == my_id) {
      player_name = "Me";
    }
    const word_list = document.createElement("div");
    word_list.classList.add('word-list');
    const player_name_line = document.createElement("p");
    player_name_line.textContent = "Player: " + player_name + ' (' + player_id + ')';
    word_list.append(player_name_line);
    for (const word of game_state.players[player_id].played_words) {
      const word_line = document.createElement("p");
      word_line.textContent = word;
      word_list.append(word_line);
    }
    UI.word_lists_container.append(word_list);
  }
}
function update_letter_display() {
  if (!game_state) {
    return;
  }
  UI.letters.textContent = game_state.letters.join(' ').toUpperCase()
}

document.addEventListener("DOMContentLoaded", function() {
  UI.canvas = document.getElementById("main_canvas");
  UI.canvas.width = 800;
  UI.canvas.height = 400;
  UI.ctx = UI.canvas.getContext('2d');
  UI.letters = document.getElementById('letters');
  UI.word_lists_container = document.getElementById('word-lists-container');
  UI.log = document.getElementById('log');
  UI.play_word_input = document.getElementById('play_word_input');
  UI.play_word_form = document.getElementById('play_word_form');
  UI.broadcast_form = document.getElementById('broadcast');
  UI.new_game_button = document.getElementById('new_game_button')

  UI.new_game_button.onclick = function (event) {
    log_msg('requesting new game');
    socket.emit('new_game_request');
  };

  // var socket = io();  // Uses html server address/port
  socket = io({
    transports: ['polling'],
    reconnection: true,
    reconnectionAttempts: 10,
    reconnectionDelay: 1000
  });
  UI.play_word_form.addEventListener('submit', (event) => {
    event.preventDefault();
    socket.emit('play_word', {data: UI.play_word_input.value});
    return false;
  });
  socket.on('letters', function(msg) {
    game_state.letters = msg.data;
    update_letter_display();
  });
  socket.on('update_game_state', function(msg) {
    game_state = msg['data'];
    comment = msg['comment'];
    console.log(game_state);
    console.log(comment);
    update_game_state_display()
  });
  socket.on('your_id', function(msg) {
    my_id = msg.data;
    log_msg('got my id:', msg, msg.data)
  });
  socket.on('connect', function(msg) {
    log_msg('connect event:', msg)
  });
  // socket.on('player_removed', function(msg) {
  //   log_msg('player_removed event:', msg)
  // });
  // socket.on('player_added', function(msg) {
  //   log_msg('player_added event:', msg)
  // });
  // socket.on('rename', function(msg) {
  //   log_msg('rename event:', msg)
  // });
  // socket.on('play_word', function(msg) {
  //   log_msg('play_word event:', msg)
  // });
  // socket.on('player_info', function(msg) {
  //   log_msg('player_info event:', msg)
  // });
  // socket.on('disconnect', function(msg) {
  //   log_msg('disconnect event:', msg)
  // });

  // broadcast_form.submit(function(event) {
  //     socket.emit('my broadcast event', {data: document.getElementById('broadcast_data').val()});
  //     return false;
  // });
});
