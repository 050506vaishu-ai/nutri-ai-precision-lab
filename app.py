import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password, full_name) VALUES (?, ?, ?)', 
                       (data['email'], data['password'], data['full_name']))
        conn.commit()
        return jsonify({"status": "success"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Email already registered"}), 400
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', 
                   (data['email'], data['password']))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=8080)