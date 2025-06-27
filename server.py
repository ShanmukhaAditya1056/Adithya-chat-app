import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("✅ Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("❌ Client disconnected")

@socketio.on('message')
def handle_message(msg):
    print("📨 Received:", msg)
    emit('message', msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
