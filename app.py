from flask import Flask, flash, request, render_template, redirect,url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3



app = Flask(__name__)
app.secret_key='higuys'

def get_db_connection():
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'user_id' in session:
        # Logged-in users see dashboard link, but homepage is still general
        return render_template('home.html', user_name=session['user_name'])
    return render_template('home.html', user_name=None)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash(' Please log in first.', 'error')
        return redirect(url_for('login'))

    return render_template('dashboard.html', user_name=session['user_name'])


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    elif request.method== 'POST':
        UserName = request.form.get('UserName').strip()
        Email = request.form.get('Email').strip().lower()
        Password = request.form.get('Password')
        conn = get_db_connection()
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
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        UserId = request.form.get('UserId').strip()
        Password = request.form.get('Password')
        conn = get_db_connection()
        cursor = conn.cursor()
        if UserId and Password:
            user = cursor.execute(
                'SELECT * FROM users WHERE name = ? OR email = ?',(UserId,UserId)
            ).fetchone()

            conn.close()

            if user is None:
                flash('User not found. Please register first','error')
                return redirect(url_for('login'))
            
            if check_password_hash(user['password_hash'], Password):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                flash(f"Welcome back, {user['name']}!",'success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect Password.','error')
                return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))
       
if __name__ == '__main__':
    app.run(debug=True)
    
