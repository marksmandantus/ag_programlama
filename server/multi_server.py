from flask import Flask, render_template, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  
socketio = SocketIO(app)

template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server')
app = Flask(__name__, template_folder=template_folder)
app.debug = True

@app.route('/')
def index():
    if 'username' in session:
        return render_template('multi-thread.html', username=session['username'])
    return render_template('multi-thread.html')

"""@socketio.on('message_from_client')
def handle_message_from_client(data):
    message = data['message']
    username = data['username']
    print(f"Message from client {username}: {message}")
    socketio.emit('message_from_server', {'username': username, 'message': message})"""

@socketio.on('user_joined')
def handle_user_joined(username):
    print(f"User joined: {username}")
    socketio.emit('message_from_server', {'username': 'SERVER', 'message': f"{username} joined the chat."})

@socketio.on('send_message')
def handle_send_message(data):
    socketio.emit('message', data, room='chat')

@socketio.on('disconnect')
def handle_disconnect():
    leave_room('chat')

if __name__ == '__main__':
    socketio.run(app)