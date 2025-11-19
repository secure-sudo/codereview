import sqlite3
from flask import Flask, request

app = Flask(_name_)

def get_db():
    conn = sqlite3.connect("users.db")
    return conn

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    # 🚨 Vulnerability #1: SQL Injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print("Executing query:", query)

    conn = get_db()
    cursor = conn.cursor()
    result = cursor.execute(query).fetchone()

    # 🚨 Vulnerability #2: Plaintext Password Check (No Hashing)
    if result:
        return f"Welcome, {username}!"
    else:
        return "Invalid credentials", 403

@app.route("/debug")
def debug():
    # 🚨 Vulnerability #3: Sensitive Debug Endpoint Exposed
    return str(dict(request.headers))

if _name_ == "_main_":
    # 🚨 Vulnerability #4: Debug Mode Enabled in Production
    app.run(host="0.0.0.0", port=5000, debug=True)
