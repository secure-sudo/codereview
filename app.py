# vulnerable_app.py
from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Insecure database setup
DB_PATH = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Vulnerable route: SQL Injection
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    c.execute(query)
    
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Login failed!"})

# Vulnerable route: Command Injection
@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host', '')
    
    # Command injection vulnerability
    result = os.popen(f'ping -c 1 {host}').read()
    return f"<pre>{result}</pre>"

# Vulnerable route: Hardcoded secret
@app.route('/secret', methods=['GET'])
def secret():
    # Hardcoded API key
    api_key = "SECRET_API_KEY_123456"
    return jsonify({"api_key": api_key})

if __name__ == '__main__':
    app.run(debug=True)
