// Загрузка данных при загрузке страницы
document.addEventListener("DOMContentLoaded", function() {
    loadBooks();

    const form = document.getElementById("add-book-form");
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        addBook();
    });
});

// Функция для загрузки списка книг
function loadBooks() {
    fetch('/api/books')
        .then(response => response.json())
        .then(books => {
            const bookList = document.querySelector('#book-list ul');
            bookList.innerHTML = '';  // Очищаем список перед добавлением новых элементов
            books.forEach(book => {
                const listItem = document.createElement('li');
                listItem.textContent = `${book.title} by ${book.author} (${book.year}) - Copies: ${book.copies}`;
                bookList.appendChild(listItem);
            });
        });
}

// Функция для добавления новой книги
function addBook() {
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const year = document.getElementById('year').value;
    const copies = document.getElementById('copies').value;

    fetch('/api/books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            author: author,
            year: year,
            copies: copies
        })
    })
    .then(response => response.json())
    .then(() => {
        loadBooks();  // Перезагружаем список книг после добавления новой
        document.getElementById('add-book-form').reset();  // Очищаем форму
    });
}

// app.js

document.addEventListener('DOMContentLoaded', function () {
    // Валидация формы добавления ученика
    const addStudentForm = document.querySelector('form[action="/add-student"]');
    if (addStudentForm) {
        addStudentForm.addEventListener('submit', function (event) {
            const name = addStudentForm.querySelector('input[name="name"]').value;
            const studentClass = addStudentForm.querySelector('input[name="class"]').value;
            const age = addStudentForm.querySelector('input[name="age"]').value;

            if (!name || !studentClass || !age) {
                alert('Please fill out all fields.');
                event.preventDefault(); // Предотвращение отправки формы
            }
        });
    }

    // Валидация формы выдачи книги
    const issueBookForm = document.querySelector('form[action="/issue-book"]');
    if (issueBookForm) {
        issueBookForm.addEventListener('submit', function (event) {
            const studentId = issueBookForm.querySelector('select[name="student_id"]').value;
            const bookId = issueBookForm.querySelector('select[name="book_id"]').value;

            if (!studentId || !bookId) {
                alert('Please select both student and book.');
                event.preventDefault(); // Предотвращение отправки формы
            }
        });
    }

    // Подтверждение перед удалением записи (например, удаление книги)
    const deleteButtons = document.querySelectorAll('.delete-button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            if (!confirm('Are you sure you want to delete this item?')) {
                event.preventDefault(); // Отменить действие, если пользователь не подтвердил
            }
        });
    });
});
