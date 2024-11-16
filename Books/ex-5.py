import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel, QFormLayout, QTableWidget, QTableWidgetItem, QDialog


# Подключение к базе данных MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Замените на ваш пароль
        database='fitness_club'
    )


# Функция для авторизации
def authenticate(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]  # Возвращаем роль (admin, trainer, client)
    return None


# Класс окна авторизации
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вход')
        self.setGeometry(100, 100, 280, 120)

        layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton('Войти', self)
        login_button.clicked.connect(self.login)

        layout.addRow('Имя пользователя', self.username_input)
        layout.addRow('Пароль', self.password_input)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        role = authenticate(username, password)

        if role:
            self.close()
            if role == 'admin':
                self.admin_window = AdminWindow()
                self.admin_window.show()
            elif role == 'trainer':
                self.trainer_window = TrainerWindow()
                self.trainer_window.show()
            else:
                self.client_window = ClientWindow()
                self.client_window.show()
        else:
            print("Неверные данные для входа")


# Класс окна администратора
class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Панель администратора')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.add_client_button = QPushButton('Добавить клиента', self)
        self.add_client_button.clicked.connect(self.add_client)

        self.add_trainer_button = QPushButton('Добавить тренера', self)
        self.add_trainer_button.clicked.connect(self.add_trainer)

        layout.addWidget(self.add_client_button)
        layout.addWidget(self.add_trainer_button)

        self.setLayout(layout)

    def add_client(self):
        self.add_client_dialog = AddClientDialog()
        self.add_client_dialog.exec_()

    def add_trainer(self):
        self.add_trainer_dialog = AddTrainerDialog()
        self.add_trainer_dialog.exec_()


# Класс окна тренера
class TrainerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Панель тренера')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.view_clients_button = QPushButton('Просмотр клиентов', self)
        self.view_clients_button.clicked.connect(self.view_clients)

        self.mark_attendance_button = QPushButton('Отметить посещаемость', self)
        self.mark_attendance_button.clicked.connect(self.mark_attendance)

        layout.addWidget(self.view_clients_button)
        layout.addWidget(self.mark_attendance_button)

        self.setLayout(layout)

    def view_clients(self):
        self.view_clients_dialog = ViewClientsDialog()
        self.view_clients_dialog.exec_()

    def mark_attendance(self):
        self.mark_attendance_dialog = MarkAttendanceDialog()
        self.mark_attendance_dialog.exec_()


# Класс окна клиента
class ClientWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Панель клиента')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.view_schedule_button = QPushButton('Просмотр расписания', self)
        self.view_schedule_button.clicked.connect(self.view_schedule)

        layout.addWidget(self.view_schedule_button)

        self.setLayout(layout)

    def view_schedule(self):
        self.view_schedule_dialog = ViewScheduleDialog()
        self.view_schedule_dialog.exec_()


# Диалог для добавления клиента
class AddClientDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить клиента')
        self.setGeometry(100, 100, 300, 150)

        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)
        self.birth_date_input = QLineEdit(self)
        self.membership_input = QLineEdit(self)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_client)

        layout = QFormLayout()
        layout.addRow('Имя:', self.first_name_input)
        layout.addRow('Фамилия:', self.last_name_input)
        layout.addRow('Дата рождения:', self.birth_date_input)
        layout.addRow('Тип абонемента:', self.membership_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_client(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        birth_date = self.birth_date_input.text()
        membership_type = self.membership_input.text()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (first_name, last_name, birth_date, membership_type) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, birth_date, membership_type))
        conn.commit()
        conn.close()
        self.accept()


# Диалог для добавления тренера
class AddTrainerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить тренера')
        self.setGeometry(100, 100, 300, 150)

        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)
        self.specialty_input = QLineEdit(self)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_trainer)

        layout = QFormLayout()
        layout.addRow('Имя:', self.first_name_input)
        layout.addRow('Фамилия:', self.last_name_input)
        layout.addRow('Специальность:', self.specialty_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_trainer(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        specialty = self.specialty_input.text()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO trainers (first_name, last_name, specialty) VALUES (%s, %s, %s)",
                       (first_name, last_name, specialty))
        conn.commit()
        conn.close()
        self.accept()


# Диалог для просмотра клиентов
class ViewClientsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Просмотр клиентов')
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Тип абонемента'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(clients))
        for row, client in enumerate(clients):
            self.table.setItem(row, 0, QTableWidgetItem(str(client[0])))
            self.table.setItem(row, 1, QTableWidgetItem(client[1]))
            self.table.setItem(row, 2, QTableWidgetItem(client[2]))
            self.table.setItem(row, 3, QTableWidgetItem(client[4]))

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)


# Диалог для отметки посещаемости
class MarkAttendanceDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Отметить посещаемость')
        self.setGeometry(100, 100, 300, 150)

        self.client_id_input = QLineEdit(self)
        self.workout_id_input = QLineEdit(self)
        self.status_input = QLineEdit(self)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_attendance)

        layout = QFormLayout()
        layout.addRow('ID клиента:', self.client_id_input)
        layout.addRow('ID тренировки:', self.workout_id_input)
        layout.addRow('Статус:', self.status_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_attendance(self):
        client_id = self.client_id_input.text()
        workout_id = self.workout_id_input.text()
        status = self.status_input.text()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO attendance (client_id, workout_id, status) VALUES (%s, %s, %s)",
                       (client_id, workout_id, status))
        conn.commit()
        conn.close()
        self.accept()


# Диалог для просмотра расписания
class ViewScheduleDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Просмотр расписания')
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID тренировки', 'Название тренировки', 'Дата'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workouts")
        workouts = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(workouts))
        for row, workout in enumerate(workouts):
            self.table.setItem(row, 0, QTableWidgetItem(str(workout[0])))
            self.table.setItem(row, 1, QTableWidgetItem(workout[2]))
            self.table.setItem(row, 2, QTableWidgetItem(str(workout[3])))

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)


# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
