Electronic-School-Library/
│
├── library.db                  # База данных SQLite (создаётся автоматически)
├── app.py                      # Основной файл приложения Flask
├── templates/                  # Шаблоны HTML
│   ├── login.html              # Страница входа в систему
│   ├── welcome.html            # Приветственная страница после авторизации
│   ├── students.html           # Страница просмотра учеников
│   ├── add_student.html        # Страница добавления ученика
│   ├── issued_books.html       # Страница просмотра выданных книг
│   └── issue_book.html         # Страница выдачи книги ученику
│
├── static/                     # Статические файлы (CSS, JS, изображения)
│   ├── styles.css              # CSS-файл для стилизации
│   └── app.js                  # JavaScript для взаимодействия на сайте
│
└── README.md                   # Описание проекта
