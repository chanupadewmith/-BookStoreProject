# app.py
# Simple CRUD System: Book Store Management System
# Python + Flask + SQL Server

from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# SQL Server Connection
# SQL Server Connection
def get_db_connection():
    server ='localhost,1434'
    database ='BookStoreDB'
    username='sa'
    password='MyStrongPass123'

    connection_string = f'''
    DRIVER={{ODBC Driver 18 for SQL Server}};
    SERVER={server};
    DATABASE={database};
    UID={username};
    PWD={password};
    Encrypt=no;
    TrustServerCertificate=yes;
    '''

    conn = pyodbc.connect(connection_string)
    return conn

# create connection
conn = get_db_connection()
cursor = conn.cursor()

# Home Page
@app.route('/')
def index():
    cursor.execute("SELECT * FROM dbo.Books")
    books = cursor.fetchall()
    return render_template("index.html", books=books)

# Add Book
@app.route('/add', methods=['POST'])
def add():
    bookid = request.form['bookid']
    title = request.form['title']
    author = request.form['author']
    price = request.form['price']

    cursor.execute(
        "INSERT INTO Books (BookID, Title, Author, Price) VALUES (?, ?, ?, ?)",
        (bookid, title, author, price)
    )
    conn.commit()
    return redirect(url_for('index'))

# Update Book
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    title = request.form['title']
    author = request.form['author']
    price = request.form['price']

    cursor.execute(
        "UPDATE Books SET Title=?, Author=?, Price=? WHERE BookID=?",
        (title, author, price, id)
    )
    conn.commit()
    return redirect(url_for('index'))

# Delete Book
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM Books WHERE BookID=?", (id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)