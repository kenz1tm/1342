from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

# Инициализация базы данных
def init_db():
    conn = get_db_connection()
    with conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class TEXT NOT NULL,
                age INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                total_copies INTEGER NOT NULL,
                available_copies INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS issued_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (book_id) REFERENCES books (id)
            );
        ''')
    conn.close()

# Главная страница — вход в систему
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'adminpass':
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

# Приветственная страница после входа
@app.route('/welcome')
def welcome():
    if 'username' not in session:
        flash('You must log in first!')
        return redirect(url_for('login'))
    return render_template('welcome.html')

# Страница для просмотра учеников
@app.route('/students')
def students():
    if 'username' not in session:
        flash('You must log in first!')
        return redirect(url_for('login'))

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('students.html', students=students)

# Страница для добавления учеников
@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if 'username' not in session:
        flash('You must log in first!')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        student_class = request.form['class']
        age = request.form['age']

        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, class, age) VALUES (?, ?, ?)', (name, student_class, age))
        conn.commit()
        conn.close()
        return redirect(url_for('students'))

    return render_template('add_student.html')

# Страница для просмотра выданных книг
@app.route('/issued-books')
def issued_books():
    if 'username' not in session:
        flash('You must log in first!')
        return redirect(url_for('login'))

    conn = get_db_connection()
    issued_books = conn.execute('''
        SELECT issued_books.id, students.name, books.title, issued_books.issue_date, issued_books.return_date
        FROM issued_books
        JOIN students ON issued_books.student_id = students.id
        JOIN books ON issued_books.book_id = books.id
    ''').fetchall()
    conn.close()
    return render_template('issued_books.html', issued_books=issued_books)

# Страница для выдачи книги ученику
@app.route('/issue-book', methods=['GET', 'POST'])
def issue_book():
    if 'username' not in session:
        flash('You must log in first!')
        return redirect(url_for('login'))

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    books = conn.execute('SELECT * FROM books').fetchall()
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        book_id = request.form['book_id']
        issue_date = datetime.now().strftime('%Y-%m-%d')

        conn.execute('INSERT INTO issued_books (student_id, book_id, issue_date) VALUES (?, ?, ?)', 
                     (student_id, book_id, issue_date))
        conn.commit()
        conn.close()
        return redirect(url_for('issued_books'))

    return render_template('issue_book.html', students=students, books=books)

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have successfully logged out.')
    return redirect(url_for('login'))

if __name__ == "__main__":
    # Инициализация базы данных
    init_db()
    app.run(debug=True)
