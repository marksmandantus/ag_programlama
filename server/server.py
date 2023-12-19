from flask import Flask, render_template
from flask_socketio import SocketIO
import os

app = Flask(__name__)
socketio = SocketIO(app)

template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server')
app = Flask(__name__, template_folder=template_folder)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message_from_client')
def handle_message_from_client(message):
    print(f"Message from client: {message}")
    socketio.emit('message_from_server', message)

if __name__ == '__main__':
    socketio.run(app, debug=True)