document.addEventListener('DOMContentLoaded', function() {
    // WebSocket connection for real-time messaging
    let socket = io.connect('http://localhost:5000', {
        extraHeaders: {
            Authorization: `Bearer ${localStorage.getItem('token')}`  // Passing the JWT token in the Authorization header
        }
    });

    const chatList = document.querySelector('.chat-list');
    const sendButton = document.getElementById('send-button')
    const messageInput = document.querySelector('.chat-input input[type="text"]');
    const chatMessages = document.querySelector('.chat-messages');
    const chatInputContainer = document.querySelector('.chat-input-container');
    const roomId = 'room1';  
    let currentRoom = null;
    let currentUser = null;
    let currentUserId = null;


    // Join a room
    socket.emit('join', { room: roomId });

    

    // Listen for incoming messages
    socket.on('receive_message', function (data) {
        console.log("receive_message");
        if (currentUser!=data.username){
        addMessage('received', `${data.username}: ${data.message}`);
    }
    });

    // Listen for system messages (join/leave notifications)
    socket.on('system_message', function (message) {
        // if (!currentUser){
        //     currentUser = data.user
        // }
        addMessage('system', message);
    });

    // Listen for broadcast notifications
    socket.on('notification', function (message) {
        displayNotification(message);
    });

    // Function to add a message to the chat window
    function addMessage(type, text) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', type);
        messageElement.innerHTML = `<p>${text}</p><span class="message-time">${new Date().toLocaleTimeString()}</span>`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to add a room to the chat list
    function addRoomToList(room) {
        const roomItem = document.createElement('div');
        roomItem.classList.add('chat-item');
        roomItem.id = `${room.id}`  // Use room name as the identifier
        roomItem.innerHTML = `
            <div class="chat-info">
                <h3>${room.name}</h3>
                <p>Click to join</p>
            </div>
        `;
        roomItem.addEventListener('click', handleChatItemClick);  // Attach click event to room
        chatList.appendChild(roomItem);
    }

    // Function to join a room
    function joinRoom(room) {
        if (currentRoom) {
            socket.emit('leave', { room: currentRoom });
        }
        currentRoom = room;
        socket.emit('join', { room: currentRoom });
        chatMessages.innerHTML = ''; // Clear the chat messages when joining a new room
        addMessage('system', `You joined ${room}`);
    } 
    // Event listener for sending a message
    // sendButton.addEventListener('click', function() {
    //     const messageText = messageInput.value;
    //     if (messageText.trim()) {
    //         addMessage('sent', messageText);
    //         messageInput.value = '';
    //         // Emit the message to the server here via WebSocket
    //         socket.emit('message', messageText);
    //     }
    // });

    // Function to display a browser push notification
    function displayNotification(message) {
        if (Notification.permission === 'granted') {
            new Notification('New Message', {
                body: message,
                icon: '/path/to/icon.png'  // Replace with the correct path to your icon
            });
        }
    }

    // Request push notification permission
    if (Notification.permission !== 'granted') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                console.log('Notification permission granted.');
            }
        });
    }

    // Load chat messages based on user selection
    async function loadChatMessages(userId) {
        const token = localStorage.getItem('token'); 
        try {
            const response = await fetch(`/chat_history/${userId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            console.log(response.ok)
            if (!response.ok) {
                throw new Error('Failed to fetch messages');
            }
            
            const data = await response.json();
            // chatInputContainer.style.display = 'flex'; // Enable the chat input container
           
            // Clear previous messages
            chatMessages.innerHTML = '';
            if(data){
            // Append new messages
            data.forEach(message => {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                messageDiv.classList.add(message.isSent ? 'sent' : 'received');

                const messageContent = document.createElement('p');
                messageContent.textContent = message.text;

                const messageTime = document.createElement('span');
                messageTime.classList.add('message-time');
                messageTime.textContent = message.time;

                messageDiv.appendChild(messageContent);
                messageDiv.appendChild(messageTime);
                chatMessages.insertBefore(messageDiv, chatMessages.firstChild);
            });
        }
        } catch (error) {
            console.error('Error fetching messages:', error);
        }
    }

    // Handle chat item click and load messages
    function handleChatItemClick(event) {
        const chatItem = event.currentTarget;
        const userId = chatItem.getAttribute('id'); // Assuming user ID is stored in the chat-item id attribute
        currentRoom = userId
        loadChatMessages(userId);
    }

    // Attach click event listeners to all chat-item elements
    document.querySelectorAll('.chat-container .sidebar .chat-list .chat-item').forEach(item => {
        item.addEventListener('click', handleChatItemClick);
    });

    

    // socket.emit('test_message', 'Hello, world!');
    //     socket.on('response', (data) => {
    //     console.log(data.message);
    //     });

    // Listening for incoming messages
    // socket.on('message', function(msg) {
    //     addMessage('received', msg);
    // });

    sendButton.addEventListener('click', function () {
        const message = messageInput.value;
        console.log(message);  // Check if the message is being correctly captured
    
        if (message.trim()) {
            const room = currentRoom;  // Assume currentRoom holds the room ID
            const username = currentUser;
            // Emit the message to the WebSocket server, along with the room ID
            socket.emit('send_message', { room: room, message: message , username: username});
            console.log("A ra");
            // Optionally add the message to the chat window for the sender
            addMessage('sent', message);
    
            // Clear the input field after sending
            messageInput.value = '';
        }
    });

    // Function to create a new chat item dynamically
    function addChatItem(user) {
        const chatItem = document.createElement('div');
        chatItem.classList.add('chat-item');
        chatItem.id = `user-${user.id}`; // Dynamically add ID using the user id

        const avatar = document.createElement('img');
        avatar.src = user.avatar;
        avatar.alt = 'User Avatar';
        avatar.classList.add('avatar');
        chatItem.appendChild(avatar);

        const chatInfo = document.createElement('div');
        chatInfo.classList.add('chat-info');

        const userName = document.createElement('h3');
        userName.textContent = user.name;
        chatInfo.appendChild(userName);

        const lastMessage = document.createElement('p');
        lastMessage.textContent = user.lastMessage;
        chatInfo.appendChild(lastMessage);

        chatItem.appendChild(chatInfo);

        const chatTime = document.createElement('span');
        chatTime.classList.add('chat-time');
        chatTime.textContent = user.time;
        chatItem.appendChild(chatTime);

        const chatList = document.querySelector('.chat-list');
        chatList.appendChild(chatItem);

        // Attach click event listener to the new chat item
        chatItem.addEventListener('click', handleChatItemClick);
    }

    // Update home page with chat items and message handling
    function update_home() {
        const token = localStorage.getItem('token');

        fetch('/auth/page_details', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`  // Add the token in the Authorization header
            }
        })
        .then(response => response.json())
        .then(data => {
            // data.forEach(user => addChatItem(user));  // Assuming API response is an array of users
            const availableRooms = [{"id":"room_1", "name":'Room 1',}]; // Replace this with an API call to fetch rooms
            currentUser = data.name
            currentUserId = data.id
            
            // Add rooms to the chat list dynamically
            availableRooms.forEach(room => addRoomToList(room));
            // Re-attach event listeners to the new chat items
            document.querySelectorAll('.chat-container .sidebar .chat-list .chat-item').forEach(item => {
                item.addEventListener('click', handleChatItemClick);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            window.location.href = '/';  // Redirect to login if unauthorized
        });
    }

    // Initial home page update to load chat items
    update_home();
});