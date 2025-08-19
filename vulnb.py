import sqlite3
import hashlib
import os
import json

# Vulnerable code: SQL Injection
def get_user_info(username, password):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    
    if user:
        return f"Welcome {user[0]}"
    else:
        return "Invalid login"

# Vulnerable code: Weak password hashing (SHA1)
def store_user_password(username, password):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Storing password in plain text (bad practice)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

    # Hashing password with SHA1 (considered weak)
    hashed_password = hashlib.sha1(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

# Vulnerable code: Input validation issues
def handle_input():
    user_input = input("Enter something: ")
    
    # No input sanitization, allowing dangerous inputs
    print(f"You entered: {user_input}")
    eval(user_input)  # Dangerous, can run arbitrary code!

# Vulnerable code: Command injection
def run_shell_command(command):
    # Command injection vulnerability
    os.system(command)

# Vulnerable code: Insecure random number generation
def generate_secure_token():
    # Using insecure random number generator
    return str(random.randint(1000, 9999))

# Vulnerable code: Exposing sensitive information
def get_config_info():
    # Exposing sensitive config data
    config = {
        'api_key': '12345',
        'db_password': 'password123',
        'username': 'admin'
    }
    
    with open('config.json', 'w') as file:
        json.dump(config, file)
    
    return "Config saved"

if __name__ == "__main__":
    print(get_user_info('admin', 'password123'))
    store_user_password('admin', 'password123')
    handle_input()
    run_shell_command('ls')
    print(generate_secure_token())
    print(get_config_info())
