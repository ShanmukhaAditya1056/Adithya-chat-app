from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB = 'users.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                avatar TEXT
            )
        ''')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = generate_password_hash(data['password'])
    avatar = data.get('avatar', '')

    try:
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO users (username, password, avatar) VALUES (?, ?, ?)",
                         (username, password, avatar))
        return jsonify({"status": "success", "message": "Registered"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"status": "fail", "message": "Username already exists"}), 409

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT password, avatar FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row and check_password_hash(row[0], password):
            return jsonify({"status": "success", "avatar": row[1]}), 200
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    init_db()
    app.run(port=8000)
