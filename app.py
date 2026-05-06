from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# 数据库初始化
def init_db():
    with sqlite3.connect('exchange.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                owner TEXT NOT NULL
            )
        ''')
    print("Database initialized!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_listing():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        owner = request.form['owner']

        with sqlite3.connect('exchange.db') as conn:
            conn.execute('INSERT INTO listings (title, description, owner) VALUES (?, ?, ?)', (title, description, owner))
            conn.commit()
        return redirect(url_for('view_listings'))
    
    return render_template('add_listing.html')

@app.route('/listings')
def view_listings():
    with sqlite3.connect('exchange.db') as conn:
        listings = conn.execute('SELECT * FROM listings').fetchall()
    return render_template('view_listings.html', listings=listings)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
