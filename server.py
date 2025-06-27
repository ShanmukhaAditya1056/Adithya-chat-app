from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')  # Must be inside a 'templates/' folder

# Chat message handler
@socketio.on('send_message')
def handle_send_message(data):
    emit('receive_message', data, broadcast=True)

# Mark message as seen
@socketio.on('message_seen')
def handle_message_seen(message_id):
    emit('mark_seen', message_id, broadcast=True)

# WebRTC call signaling events
@socketio.on('offer')
def handle_offer(offer):
    emit('offer', offer, broadcast=True)

@socketio.on('answer')
def handle_answer(answer):
    emit('answer', answer, broadcast=True)

@socketio.on('ice')
def handle_ice(candidate):
    emit('ice', candidate, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
