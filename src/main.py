from flask import Flask, request, render_template
import sqlite3
import pretty_errors
import random
import string
import os
import hashlib


app = Flask(__name__)

connection = sqlite3.connect('records.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT,
        username TEXT,
        email TEXT,
        password TEXT,
        verified BOOLEAN
    )
""")
connection.commit()

def generate_uid():
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    unique = False

    while not unique:
        cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        unique=True
        for _ in cursor.fetchall():
            unique=False
            id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    return id

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

# @app.route('/')
# def debug():
#     cursor.execute("SELECT * FROM users")
#     items = cursor.fetchall()
#     return render_template('debug.html', items=items)


@app.route('/user/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form['username']
        email = request.form['email']
        password = encrypt_string(request.form['password'])
        id = generate_uid()

        cursor.execute("INSERT INTO users VALUES(?,?,?,?,?)", (id, username, email, password, False))

        return 'Registered'
    
@app.route('/user/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form['email']
        password = encrypt_string(request.form['password'])

        cursor.execute("SELECT id FROM users WHERE email=? and password=?", (email, password))

        if len(cursor.fetchall()) > 0:
            return 'logined!'
        else:
            return "email or password not correct!"

if __name__ == "__main__":
    app.run(debug=True)
    connection.commit()
    connection.close()