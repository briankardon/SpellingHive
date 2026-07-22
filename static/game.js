var UI = {}
var game_state;
var socket;
var my_id;

function go_to_lobby() {
  window.location.href = '/lobby';
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
  console.log('updating letters:', game_state.letters);
  UI.letters.textContent = game_state.letters.join(' ').toUpperCase()
}

function show_message(message) {
  const new_message = document.createElement("span");
  new_message.textContent = message;
  new_message.classList.add('message');
  UI.messages.append(new_message);
  setTimeout(
    function() {new_message.remove()},
    4000
  )
}

document.addEventListener("DOMContentLoaded", function() {
  UI.canvas = document.getElementById("main_canvas");
  UI.canvas.width = 400;
  UI.canvas.height = 200;
  UI.ctx = UI.canvas.getContext('2d');
  UI.letters = document.getElementById('letters');
  UI.word_lists_container = document.getElementById('word-lists-container');
  UI.log = document.getElementById('log');
  UI.play_word_input = document.getElementById('play_word_input');
  UI.end_game_button = document.getElementById('end_game_button');
  UI.chat_input = document.getElementById('chat_input');
  UI.messages = document.getElementById('messages');

  UI.end_game_button.onclick = function (event) {
    socket.emit('new_game_request');
  };

  // var socket = io();  // Uses html server address/port
  socket = io({
    transports: ['polling'],
    reconnection: true,
    reconnectionAttempts: 10,
    reconnectionDelay: 1000
  });

  UI.play_word_input.addEventListener('keydown', function(event) {
    // Check if the pressed key is "Enter"
    if (event.key === 'Enter') {
      event.preventDefault();
      socket.emit('play_word', {data: UI.play_word_input.value});
      return false;
    }
  });
  UI.chat_input.addEventListener('keydown', function(event) {
    // Check if the pressed key is "Enter"
    if (event.key === 'Enter') {
      socket.emit('chat', {data: UI.chat_input.value});
      UI.chat_input.value = '';
    }
  });
  socket.on('letters', function(msg) {
    game_state.letters = msg.data;
    update_letter_display();
  });
  socket.on('update_game_state', function(msg) {
    game_state = msg['data'];
    if (!game_state.started) {
      // Game hasn't started yet
      console.log('game has not started, redirecting to lobby');
      go_to_lobby();
      return;
    }
    comment = msg['comment'];
    show_message(comment);
    update_game_state_display()
  });
  socket.on('your_id', function(msg) {
    my_id = msg.data;
  });
  socket.on('connect', function(msg) {
  });

  socket.on('message', function(msg) {
    show_message(msg.data);
  });

  // Request a new game from server
  socket.emit('new_game_request');

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
