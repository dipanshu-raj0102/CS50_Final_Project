from flask import Flask,request, render_template, redirect,url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3



app = Flask(__name__)
app.secret_key='higuys'

def get_db_connections():
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    elif request.method== 'POST':
        UserName = request.form.get('UserName').strip()
        Email = request.form.get('Email').strip().lower()
        Password = request.form.get('Password')
        conn = get_db_connections()
        cursor = conn.cursor()
        if UserName and Password and Email:
            existing_user = cursor.execute(
                'SELECT * FROM users WHERE name = ? OR email = ?',(UserName,Email)).fetchone()
            if existing_user:
                flash('UserName or Email already exist. Please choose another.', 'error')
                conn.close()
                return redirect(url_for('register'))
            else:
                pass_hash = generate_password_hash(Password)
                cursor.execute(
                    'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',(UserName, Email, pass_hash)    
                )
                conn.commit()
                conn.close()

                flash('Registration successful! You can now login', 'success')
                return redirect(url_for('login'))
        else:
            flash('Please fill each box','error')
            return redirect(url_for('register'))
        
@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')
          
        
if __name__ == '__main__':
    app.run(debug=True)
    
