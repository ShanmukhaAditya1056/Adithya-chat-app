from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet

eventlet.monkey_patch()  # Needed for SocketIO to work with eventlet

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allows any frontend

@app.route('/')
def index():
    return render_template('index.html')  # Renders the chat UI

@socketio.on('message')
def handle_message(msg):
    print('Received message:', msg)
    emit('message', msg, broadcast=True)  # Broadcasts to all connected clients

@socketio.on('connect')
def on_connect():
    print("Client connected")

@socketio.on('disconnect')
def on_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)  # Works for local and Render
