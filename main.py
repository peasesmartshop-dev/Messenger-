import os
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bulochnaya'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Список для хранения последних 50 сообщений
history = []

@app.route('/')
def index():
    return "Сервер мессенджера запущен!"

@socketio.on('connect')
def handle_connect():
    # Когда кто-то заходит, отправляем ему всю историю
    for msg in history:
        emit('message', msg)

@socketio.on('message')
def handle_message(msg):
    history.append(msg)
    if len(history) > 50: history.pop(0) # Храним только последние 50
    print(f"Новое сообщение: {msg}")
    emit('message', msg, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
    
