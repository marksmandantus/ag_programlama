import threading
import time
import socketio

sio = socketio.Client()

@sio.on('message_from_server')
def handle_message_from_server(data):
    print(f"Message from server: {data['username']}: {data['message']}")

def send_messages():
    while True:
        message = input("Client message: ")
        username = input("Enter your username: ")
        sio.emit('message_from_client', {'username': username, 'message': message})
        time.sleep(1)

if __name__ == '__main__':
    server_url = 'http://127.0.0.1:5000'
    sio.connect(server_url, namespaces=['/'])

    thread = threading.Thread(target=send_messages)
    thread.start()

    sio.wait()