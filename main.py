import os, json
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bulochnaya'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

USERS_FILE = 'users.json'
history = []

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f: return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f: json.dump(users, f)

users_db = load_users()

@socketio.on('register')
def handle_register(data):
    u, p = data.get('user'), data.get('pass')
    if u in users_db:
        emit('auth_res', {'ok': False, 'msg': 'Имя занято'})
    else:
        users_db[u] = p
        save_users(users_db)
        emit('auth_res', {'ok': True, 'msg': 'Регистрация успешна'})

@socketio.on('login')
def handle_login(data):
    u, p = data.get('user'), data.get('pass')
    if users_db.get(u) == p:
        emit('auth_res', {'ok': True, 'msg': 'Вход выполнен'})
        for msg in history: emit('message', msg)
    else:
        emit('auth_res', {'ok': False, 'msg': 'Неверный логин/пароль'})

@socketio.on('message')
def handle_message(msg):
    history.append(msg)
    if len(history) > 50: history.pop(0)
    emit('message', msg, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
    
    
