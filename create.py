import sqlite3

# Подключение к базе данных (если файла нет, он будет создан)
conn = sqlite3.connect('library.db')

# Создание курсора для выполнения SQL-запросов
c = conn.cursor()

# Создание таблицы books
c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        copies INTEGER
    )
''')

c.execute('''
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        class TEXT NOT NULL,
        age INTEGER NOT NULL
    );
''')

c.execute('''
    CREATE TABLE issued_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        issue_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (book_id) REFERENCES books (id)
    );
''')

# Подтверждение изменений и закрытие подключения
conn.commit()
conn.close()

print("Database and table 'books' created successfully.")
