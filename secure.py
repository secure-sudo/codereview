import os
from flask import Flask, request, jsonify, render_template_string
import sqlite3  # Example DB
from markupsafe import escape

app = Flask(__name__)

# ✅ Disable debug mode in production
app.config['DEBUG'] = False

# ✅ Load DB credentials from environment variables
DB_PATH = os.getenv("DB_PATH", "test.db")  # Use environment variable or default

# Helper function to get DB connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<int:user_id>')
def get_user(user_id):
    """
    ✅ Use parameterized queries to prevent SQL injection
    """
    conn = get_db_connection()
    user = conn.execute("SELECT username, email FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    if user:
        return jsonify({"username": user["username"], "email": user["email"]})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/ping')
def ping():
    """
    ✅ Escape output to prevent XSS
    """
    message = request.args.get("message", "pong")
    safe_message = escape(message)
    return render_template_string("<p>{{ message }}</p>", message=safe_message)

# ✅ No os.system or subprocess calls -> prevent command injection

if __name__ == '__main__':
    # ✅ Production-safe: debug=False
    app.run(host='0.0.0.0', port=5000, debug=False)
