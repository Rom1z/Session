import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from getpass import getpass

# Подключение к базе данных MySQL
db = mysql.connector.connect (
    host="localhost" ,
    user="root" ,
    password="" ,  # Укажите свой пароль
    database="work_time_tracking"
)
cursor = db.cursor ()


# Функция авторизации пользователя
def authorize():
    username = username_entry.get ()
    password = password_entry.get ()

    cursor.execute ( "SELECT role, employee_id FROM Employees WHERE name=%s AND password=%s" , (username , password) )
    result = cursor.fetchone ()

    if result:
        global user_role , employee_id
        user_role , employee_id = result
        messagebox.showinfo ( "Успех" , f"Добро пожаловать, {username} ({user_role})!" )
        open_main_menu ()
    else:
        messagebox.showerror ( "Ошибка" , "Неправильное имя пользователя или пароль." )


# Функция добавления рабочего времени
def add_work_hours():
    date = date_entry.get ()
    hours_worked = hours_entry.get ()
    description = description_entry.get ()

    if not date or not hours_worked or not description:
        messagebox.showerror ( "Ошибка" , "Пожалуйста, заполните все поля." )
        return

    try:
        cursor.execute (
            "INSERT INTO WorkHours (employee_id, date, hours_worked, description) VALUES (%s, %s, %s, %s)" ,
            (employee_id , date , float ( hours_worked ) , description) )
        db.commit ()
        messagebox.showinfo ( "Успех" , "Рабочее время добавлено." )
    except Exception as e:
        messagebox.showerror ( "Ошибка" , f"Не удалось добавить рабочее время: {e}" )


# Функция отображения рабочего времени сотрудника
def view_work_hours():
    cursor.execute ( "SELECT date, hours_worked, description FROM WorkHours WHERE employee_id = %s" , (employee_id ,) )
    records = cursor.fetchall ()
    work_hours_text.delete ( "1.0" , tk.END )  # Очистка текстового поля

    if not records:
        work_hours_text.insert ( tk.END , "Нет записей о рабочем времени." )
    else:
        for record in records:
            date , hours , desc = record
            work_hours_text.insert ( tk.END , f"Дата: {date}, Часы: {hours}, Описание: {desc}\n" )


# Окно авторизации
def create_login_window():
    global username_entry , password_entry

    login_window = tk.Tk ()
    login_window.title ( "Авторизация" )
    tk.Label ( login_window , text="Имя пользователя:" ).grid ( row=0 , column=0 )
    tk.Label ( login_window , text="Пароль:" ).grid ( row=1 , column=0 )

    username_entry = tk.Entry ( login_window )
    password_entry = tk.Entry ( login_window , show="*" )
    username_entry.grid ( row=0 , column=1 )
    password_entry.grid ( row=1 , column=1 )

    login_button = tk.Button ( login_window , text="Войти" , command=authorize )
    login_button.grid ( row=2 , column=1 )

    login_window.mainloop ()


# Главное меню
def open_main_menu():
    main_window = tk.Tk ()
    main_window.title ( "Учет рабочего времени" )

    # Панель добавления рабочего времени
    tk.Label ( main_window , text="Дата (YYYY-MM-DD):" ).grid ( row=0 , column=0 )
    tk.Label ( main_window , text="Часы:" ).grid ( row=1 , column=0 )
    tk.Label ( main_window , text="Описание:" ).grid ( row=2 , column=0 )

    global date_entry , hours_entry , description_entry , work_hours_text
    date_entry = tk.Entry ( main_window )
    hours_entry = tk.Entry ( main_window )
    description_entry = tk.Entry ( main_window )
    date_entry.grid ( row=0 , column=1 )
    hours_entry.grid ( row=1 , column=1 )
    description_entry.grid ( row=2 , column=1 )

    add_button = tk.Button ( main_window , text="Добавить рабочее время" , command=add_work_hours )
    add_button.grid ( row=3 , column=1 )

    # Панель для просмотра рабочего времени
    work_hours_text = tk.Text ( main_window , height=10 , width=50 )
    work_hours_text.grid ( row=4 , column=0 , columnspan=2 )
    view_button = tk.Button ( main_window , text="Просмотреть рабочее время" , command=view_work_hours )
    view_button.grid ( row=5 , column=1 )

    main_window.mainloop ()


# Запуск окна авторизации
create_login_window ()

# Закрытие соединения с базой данных при завершении
cursor.close ()
db.close ()
