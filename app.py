from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/multi-thread')
def multi_thread():
    return render_template('multi-thread.html')

@socketio.on('message_from_client')
def handle_message_from_client(message):
    print(f"Message from client: {message}")
    socketio.emit('message_from_server', f"Server says: {message}")

@socketio.on('message_from_server')
def handle_message_from_server(message):
    print(f"Message from server: {message}")
    socketio.emit('message_from_client', f"Client says: {message}")

@socketio.on('user_joined')
def handle_user_joined(username):
    socketio.emit('message', {'username': 'SERVER', 'message': f'{username} joined the chat'})

@socketio.on('send_message')
def handle_send_message(data):
    socketio.emit('message', data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
