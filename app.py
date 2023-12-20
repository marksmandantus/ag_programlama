from flask import Flask, render_template, request
from flask_socketio import SocketIO
import requests
import time
app = Flask(__name__)
socketio = SocketIO(app)
import threading

# API key ve base URL
ACCESS_KEY = '70b44b807114df0f9eb8ca113951ad86'
URL = f'http://data.fixer.io/api/latest?access_key={ACCESS_KEY}'

def get_exchange_rate(from_currency, to_currency):
    response = requests.get(URL)
    rates = response.json()['rates']
    
    if from_currency == 'EUR':
        rate = rates[to_currency]
    elif to_currency == 'EUR':
        rate = 1 / rates[from_currency]
    else:
        rate = rates[to_currency] / rates[from_currency]

    return rate

def update_exchange_rate():
    while True:
        rate = get_exchange_rate("USD", "TRY")
        converted_amount = round(rate, 5)
        print(converted_amount)
        socketio.emit('update_rate', {'rate': converted_amount})
        time.sleep(10)  # Örneğin, her dakikada bir güncelle

        

@app.route('/convert')
def convert():
    #from_currency = request.form['from_currency']
    #to_currency = request.form['to_currency']
    #amount = float(request.form['amount'])
    #from_currency = "USD"
    #to_currency = "TRY"
    #amount=1
    return render_template('result.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/multi-thread')
def multi_thread():
    return render_template('multi-thread.html')

# @app.route('/dynamic')
# def dynamic():
#     return render_template('result.html')

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
    
    # Arka planda oranı güncelleyen bir thread başlat
    update_thread = threading.Thread(target=update_exchange_rate)
    update_thread.daemon = True
    update_thread.start()
    socketio.run(app, debug=True)