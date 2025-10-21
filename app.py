from flask import Flask, render_template
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

def get_deb_connections():
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
    