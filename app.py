from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

# 👇 DB initialize karega agar table nahi bana
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

# ⚙️ Init DB at server start
init_db()

# 🏠 Home route
@app.route('/')
def index():
    conn = sqlite3.connect('renters.db')
    c = conn.cursor()
    c.execute("SELECT * FROM renters ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return render_template("index.html", renters=data)

# ➕ Add renter route
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    number = request.form['number']
    amount = int(request.form['amount'])
    paid = int(request.form['paid'])
    month = request.form['month']
    now = datetime.datetime.now().strftime("%I:%M %p %d-%b-%Y")

    conn = sqlite3.connect('renters.db')
    c = conn.cursor()
    c.execute("INSERT INTO renters (name, number, amount, paid, month, time) VALUES (?, ?, ?, ?, ?, ?)",
              (name, number, amount, paid, month, now))
    conn.commit()
    conn.close()
    return redirect('/')

# ✅ Run app on 0.0.0.0
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
