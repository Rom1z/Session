import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date

# Настройка подключения к базе данных
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Замените на ваш MySQL пользователь
    password="",  # Замените на ваш MySQL пароль
    database="library"  # Замените на название вашей базы данных
)
cursor = conn.cursor()


# Функция для авторизации
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Проверка пользователя в базе данных
    cursor.execute("SELECT role FROM Users WHERE name=%s AND password=%s", (username, password))
    result = cursor.fetchone()

    if result:
        role = result[0]
        login_window.destroy()
        open_main_window(role)
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")


# Главное окно
def open_main_window(role):
    main_window = tk.Tk()
    main_window.title("Управление библиотекой")

    if role == 'Администратор' or role == 'Библиотекарь':
        tk.Button(main_window, text="Добавить книгу", command=add_book_window).pack(pady=5)
        tk.Button(main_window, text="Редактировать книгу", command=edit_book_window).pack(pady=5)
        tk.Button(main_window, text="Удалить книгу", command=delete_book_window).pack(pady=5)

    if role == 'Читатель' or role == 'Библиотекарь' or role == 'Администратор':
        tk.Button(main_window, text="Выдать книгу", command=borrow_book_window).pack(pady=5)
        tk.Button(main_window, text="Вернуть книгу", command=return_book_window).pack(pady=5)

    main_window.mainloop()


# Окно добавления книги
def add_book_window():
    def add_book():
        title = title_entry.get()
        author = author_entry.get()
        genre = genre_entry.get()
        year = year_entry.get()

        # Исправлена ошибка: 'author' вместо 'writer'
        cursor.execute(
            "INSERT INTO Books (title, author, genre, year) VALUES (%s, %s, %s, %s)",
            (title, author, genre, year)
        )

        conn.commit()
        messagebox.showinfo("Успешно", "Книга добавлена")

    add_window = tk.Toplevel()
    add_window.title("Добавить книгу")

    tk.Label(add_window, text="Название").grid(row=0, column=0)
    title_entry = tk.Entry(add_window)
    title_entry.grid(row=0, column=1)

    tk.Label(add_window, text="Автор").grid(row=1, column=0)
    author_entry = tk.Entry(add_window)
    author_entry.grid(row=1, column=1)

    tk.Label(add_window, text="Жанр").grid(row=2, column=0)
    genre_entry = tk.Entry(add_window)
    genre_entry.grid(row=2, column=1)

    tk.Label(add_window, text="Год").grid(row=3, column=0)
    year_entry = tk.Entry(add_window)
    year_entry.grid(row=3, column=1)

    tk.Button(add_window, text="Добавить", command=add_book).grid(row=4, column=1)


# Окно редактирования книги
def edit_book_window():
    def update_book():
        book_id = id_entry.get()
        title = title_entry.get()
        author = author_entry.get()
        genre = genre_entry.get()
        year = year_entry.get()

        cursor.execute(
            "UPDATE Books SET title=%s, author=%s, genre=%s, year=%s WHERE book_id=%s",
            (title, author, genre, year, book_id)
        )
        conn.commit()
        messagebox.showinfo("Успешно", "Книга обновлена")

    edit_window = tk.Toplevel()
    edit_window.title("Редактировать книгу")

    tk.Label(edit_window, text="ID книги").grid(row=0, column=0)
    id_entry = tk.Entry(edit_window)
    id_entry.grid(row=0, column=1)

    tk.Label(edit_window, text="Название").grid(row=1, column=0)
    title_entry = tk.Entry(edit_window)
    title_entry.grid(row=1, column=1)

    tk.Label(edit_window, text="Автор").grid(row=2, column=0)
    author_entry = tk.Entry(edit_window)
    author_entry.grid(row=2, column=1)

    tk.Label(edit_window, text="Жанр").grid(row=3, column=0)
    genre_entry = tk.Entry(edit_window)
    genre_entry.grid(row=3, column=1)

    tk.Label(edit_window, text="Год").grid(row=4, column=0)
    year_entry = tk.Entry(edit_window)
    year_entry.grid(row=4, column=1)

    tk.Button(edit_window, text="Обновить", command=update_book).grid(row=5, column=1)


# Окно удаления книги
def delete_book_window():
    def delete_book():
        book_id = id_entry.get()
        cursor.execute("DELETE FROM Books WHERE book_id=%s", (book_id,))
        conn.commit()
        messagebox.showinfo("Успешно", "Книга удалена")

    delete_window = tk.Toplevel()
    delete_window.title("Удалить книгу")

    tk.Label(delete_window, text="ID книги").grid(row=0, column=0)
    id_entry = tk.Entry(delete_window)
    id_entry.grid(row=0, column=1)

    tk.Button(delete_window, text="Удалить", command=delete_book).grid(row=1, column=1)


# Окно выдачи книги
def borrow_book_window():
    def borrow_book():
        book_id = book_id_entry.get()
        user_id = user_id_entry.get()
        cursor.execute(
            "INSERT INTO Borrows (book_id, user_id, borrow_date) VALUES (%s, %s, %s)",
            (book_id, user_id, date.today())
        )
        conn.commit()
        messagebox.showinfo("Успешно", "Книга выдана")

    borrow_window = tk.Toplevel()
    borrow_window.title("Выдать книгу")

    tk.Label(borrow_window, text="ID книги").grid(row=0, column=0)
    book_id_entry = tk.Entry(borrow_window)
    book_id_entry.grid(row=0, column=1)

    tk.Label(borrow_window, text="ID пользователя").grid(row=1, column=0)
    user_id_entry = tk.Entry(borrow_window)
    user_id_entry.grid(row=1, column=1)

    tk.Button(borrow_window, text="Выдать", command=borrow_book).grid(row=2, column=1)


# Окно возврата книги
def return_book_window():
    def return_book():
        borrow_id = borrow_id_entry.get()
        cursor.execute(
            "UPDATE Borrows SET return_date=%s WHERE borrow_id=%s",
            (date.today(), borrow_id)
        )
        conn.commit()
        messagebox.showinfo("Успешно", "Книга возвращена")

    return_window = tk.Toplevel()
    return_window.title("Вернуть книгу")

    tk.Label(return_window, text="ID выдачи").grid(row=0, column=0)
    borrow_id_entry = tk.Entry(return_window)
    borrow_id_entry.grid(row=0, column=1)

    tk.Button(return_window, text="Вернуть", command=return_book).grid(row=1, column=1)


# Окно авторизации
login_window = tk.Tk()
login_window.title("Авторизация")

tk.Label(login_window, text="Имя пользователя").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Пароль").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Войти", command=login).pack()

login_window.mainloop()
