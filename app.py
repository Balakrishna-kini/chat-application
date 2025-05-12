from flask import Flask, render_template_string
from flask_socketio import SocketIO, send

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # Required for SocketIO sessions

# Initialize SocketIO with Flask app
socketio = SocketIO(app, cors_allowed_origins="*")

# Simple HTML template for the chat UI
chat_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        #messages { list-style-type: none; padding: 0; max-height: 300px; overflow-y: scroll; border: 1px solid #ccc; }
        #messages li { padding: 5px 10px; }
        input { padding: 10px; width: 70%; }
        button { padding: 10px; }
    </style>
</head>
<body>
    <h2>Real-Time Chat App</h2>
    <ul id="messages"></ul>
    <input id="msgInput" autocomplete="off" placeholder="Type a message...">
    <button onclick="sendMsg()">Send</button>

    <script src="https://cdn.socket.io/4.6.1/socket.io.min.js"></script>
    <script>
        var socket = io();

        socket.on('message', function(msg) {
            var item = document.createElement('li');
            item.textContent = msg;
            document.getElementById('messages').appendChild(item);
        });

        function sendMsg() {
            var input = document.getElementById('msgInput');
            var message = input.value;
            if (message.trim() !== "") {
                socket.send(message);
                input.value = '';
            }
        }
    </script>
</body>
</html>
"""

# Route to serve the chat page
@app.route('/')
def index():
    return render_template_string(chat_page)

# SocketIO event for handling incoming messages
@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)
    send(msg, broadcast=True)

# Run the app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)
