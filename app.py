from flask import Flask, flash, request, render_template, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime



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
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        transactions = cursor.execute(
            """SELECT t.id, t.amount, t.date, t.note, c.name AS category_name, c.type AS category_type FROM transactions t JOIN categories c ON t.category_id = c.id WHERE t.user_id = ?
            ORDER BY date(t.date) DESC
            """, (session['user_id'],)).fetchall()
        totals = cursor.execute(
                """SELECT 
                SUM(CASE WHEN c.type='income' THEN t.amount ELSE 0 END) AS total_income,
                SUM(CASE WHEN c.type='expense' THEN t.amount ELSE 0 END) AS total_expense
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                WHERE t.user_id = ?
                """, (session['user_id'],)).fetchone()

    # Expense per category
        category_expense = cursor.execute(
            """SELECT c.name AS category_name, SUM(t.amount) AS total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = ? AND c.type='expense'
            GROUP BY c.name
            """, (session['user_id'],)).fetchall()

        conn.close()

        return render_template('dashboard.html', user_name=session['user_name'], transactions = transactions, totals=totals, category_expense=category_expense)


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
                'SELECT * FROM users WHERE name = ? OR email = ?',(UserId, UserId)
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

@app.route('/add_transaction', methods = ['POST','GET'])
def add_transaction():
    if request.method == "GET":
        user_id = session.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        categories = cursor.execute(
            "SELECT * FROM categories WHERE user_id IS NULL OR user_id = ?", (user_id,)
        ).fetchall()
        conn.close()
        return render_template("add_transaction_form.html", categories=categories)
    elif request.method == 'POST':
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        date = request.form.get('date')
        note = request.form.get('note')
        user_id = session.get("user_id")
        conn = get_db_connection()
        cursor = conn.cursor()
        if user_id and category_id and amount and date:
            cursor.execute(
                "INSERT INTO transactions (user_id, category_id, amount, date, note) VALUES (?, ?, ?, ?, ?)",
                (user_id, category_id, amount, date, note),
            )
            conn.commit()
            conn.close()
            flash("Transaction added successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Please fill all the details", "error")
            conn.close()

@app.route('/delete_txn/<int:txn_id>', methods=['POST'])
def delete_txn(txn_id):
    if 'user_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete only if the transaction belongs to logged-in user
    cursor.execute(
        "DELETE FROM transactions WHERE id = ? AND user_id = ?",
        (txn_id, session['user_id'])
    )

    conn.commit()
    conn.close()

    flash("Transaction deleted successfully!", "success")
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
    
