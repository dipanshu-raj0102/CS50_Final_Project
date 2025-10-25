Smart Finance Manager
    A personal finance web app that helps you track, visualize, and manage your money smartly — built with Flask, SQLite, Bootstrap 5, and Chart.js.

Live Demo
    Deployed at: https://cs50-final-project-70l0.onrender.com

    Demo Video: https://youtu.be/s3LkWEFBR8k

Tech Stack
    Frontend: HTML, CSS, Bootstrap 5, Chart.js
    Backend: Flask (Python)
    Database: SQLite
    Deployment: Render
    Authentication: Werkzeug (hashed passwords + sessions)

Key Features
    Secure user registration and login
    Add, edit, and delete transactions
    Categorize transactions as income or expense
    Real-time dashboard with totals and balance
    Visual analytics with Chart.js
    Expense breakdown by category
    Beautiful gradient UI and responsive layout

Database
    finance.db includes 3 main tables:
    users — stores user credentials
    categories — stores income/expense categories
    transactions — stores all user transactions

Installation & Run Locally
    Clone the repo
        git clone https://github.com/dipanshu-raj0102/CS50_Final_Project.git
        cd CS50_Final_Project


    Create a virtual environment
        python -m venv venv
        source venv/bin/activate  # on Windows: venv\Scripts\activate

    Install dependencies
        pip install -r requirements.txt

    Run the app
        flask run  or python app.py

Author
    Dipanshu Raj
    dipanshuraj0102@gmail.com
    CS50x Final Project — 2025
    Deployed via Render