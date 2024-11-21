// const socket = io.connect('http://localhost:5000');
// const messageInput = document.getElementById('message-input');
// const chatMessages = document.getElementById('chat-messages');

// document.getElementById('send-button').addEventListener('click', function() {
//     const message = messageInput.value;
//     socket.emit('message', message);
//     messageInput.value = '';
// });

// socket.on('message', function(msg) {
//     const messageElement = document.createElement('div');
//     messageElement.textContent = msg;
//     chatMessages.appendChild(messageElement);
// });

// const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

document.getElementById("submit").onclick = function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem('token', data.access_token);
        console.log(data.access_token);
        // window.location.headers = {"access_token": data.access_token}
        window.location.href = '/home';
    });
};

// socket.on('receive_message', function(data) {
//     const chatWindow = document.getElementById('chat-window');
//     const messageElement = document.createElement('p');
//     messageElement.textContent = `${data.user}: ${data.msg}`;
//     chatWindow.appendChild(messageElement);
// });

// document.getElementById('send').onclick = function() {
//     const message = document.getElementById('message').value;
//     const token = localStorage.getItem('token');
//     socket.emit('send_message', { message, room: 'general', token });
// };
