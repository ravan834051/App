from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ✅ Create DB if not exists
def init_db():
    conn = sqlite3.connect('rent.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS renters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    monthly_rent INTEGER,
                    paid INTEGER,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('rent.db')
    c = conn.cursor()
    c.execute("SELECT * FROM renters ORDER BY timestamp DESC")
    renters = c.fetchall()
    conn.close()
    return render_template('index.html', renters=renters)

@app.route('/add', methods=['POST'])
def add_renter():
    name = request.form['name']
    phone = request.form['phone']
    rent = int(request.form['monthly_rent'])
    paid = int(request.form['paid'])
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    
    conn = sqlite3.connect('rent.db')
    c = conn.cursor()
    c.execute("INSERT INTO renters (name, phone, monthly_rent, paid, timestamp) VALUES (?, ?, ?, ?, ?)",
              (name, phone, rent, paid, timestamp))
    conn.commit()
    conn.close()

    return redirect('/')

import sqlite3

def init_db():
    conn = sqlite3.connect('renters.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS renters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    number TEXT NOT NULL,
                    amount INTEGER,
                    paid INTEGER,
                    month TEXT,
                    time TEXT
                )''')
    conn.commit()
    conn.close()

init_db()  # Call this when app starts

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
