from flask import Flask, render_template
from flask_socketio import SocketIO, send
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    print('Message received: ' + msg)
    try:
        # Try to parse as JSON to check if it's a typing indicator
        data = json.loads(msg)
        if 'type' in data and data['type'] == 'typing':
            # Forward typing indicator to all clients
            socketio.emit('typing', msg)
            return
    except:
        # Not JSON or not a typing indicator, treat as regular message
        pass
    
    # Forward the message to all clients
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)