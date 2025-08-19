import sqlite3
import hashlib

def get_user_info(username, password):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    if user:
        return f"Welcome {user[0]}"
    else:
        return "Invalid login"

def store_user_password(username, password):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

def handle_input():
    user_input = input("Enter something: ")
    print(f"You entered: {user_input}")
    eval(user_input)

if __name__ == "__main__":
    print(get_user_info('admin', 'password123'))
    store_user_password('admin', 'password123')
    handle_input()
