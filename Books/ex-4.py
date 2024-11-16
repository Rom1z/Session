import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QFormLayout, QLabel, \
    QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox, QComboBox

# Подключение к базе данных MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Замените на ваш пароль
        database='educational_center'
    )

# Функция для авторизации
def authenticate(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]  # Возвращаем роль (admin, teacher, student)
    return None

# Класс окна авторизации
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
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
            elif role == 'teacher':
                self.teacher_window = TeacherWindow()
                self.teacher_window.show()
            else:
                self.student_window = StudentWindow()
                self.student_window.show()
        else:
            print("Неверные данные для входа")

# Класс окна администратора
class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Панель администратора')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.add_student_button = QPushButton('Добавить студента', self)
        self.add_student_button.clicked.connect(self.add_student)

        self.add_course_button = QPushButton('Добавить курс', self)
        self.add_course_button.clicked.connect(self.add_course)

        self.view_students_button = QPushButton('Просмотр студентов', self)
        self.view_students_button.clicked.connect(self.view_students)

        self.view_courses_button = QPushButton('Просмотр курсов', self)
        self.view_courses_button.clicked.connect(self.view_courses)

        layout.addWidget(self.add_student_button)
        layout.addWidget(self.add_course_button)
        layout.addWidget(self.view_students_button)
        layout.addWidget(self.view_courses_button)

        self.setLayout(layout)

    def add_student(self):
        self.add_student_dialog = AddStudentDialog()
        self.add_student_dialog.exec_()

    def add_course(self):
        self.add_course_dialog = AddCourseDialog()
        self.add_course_dialog.exec_()

    def view_students(self):
        self.view_students_dialog = ViewStudentsDialog()
        self.view_students_dialog.exec_()

    def view_courses(self):
        self.view_courses_dialog = ViewCoursesDialog()
        self.view_courses_dialog.exec_()

# Класс окна преподавателя
class TeacherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Панель преподавателя')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.view_students_button = QPushButton('Просмотр студентов', self)
        self.view_students_button.clicked.connect(self.view_students)

        self.mark_attendance_button = QPushButton('Учет посещаемости', self)
        self.mark_attendance_button.clicked.connect(self.mark_attendance)

        layout.addWidget(self.view_students_button)
        layout.addWidget(self.mark_attendance_button)

        self.setLayout(layout)

    def view_students(self):
        self.view_students_dialog = ViewStudentsDialog()
        self.view_students_dialog.exec_()

    def mark_attendance(self):
        self.mark_attendance_dialog = MarkAttendanceDialog()
        self.mark_attendance_dialog.exec_()

# Класс окна студента
class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Панель студента')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.view_courses_button = QPushButton('Просмотр курсов', self)
        self.view_courses_button.clicked.connect(self.view_courses)

        layout.addWidget(self.view_courses_button)

        self.setLayout(layout)

    def view_courses(self):
        self.view_courses_dialog = ViewCoursesDialog()
        self.view_courses_dialog.exec_()

# Диалог для добавления студента
class AddStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить студента')
        self.setGeometry(100, 100, 300, 150)

        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_student)

        layout = QFormLayout()
        layout.addRow('Имя:', self.first_name_input)
        layout.addRow('Фамилия:', self.last_name_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_student(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()

        if first_name and last_name:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (first_name, last_name) VALUES (%s, %s)",
                           (first_name, last_name))
            conn.commit()
            conn.close()
            self.accept()

# Диалог для добавления курса
class AddCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить курс')
        self.setGeometry(100, 100, 300, 150)

        self.name_input = QLineEdit(self)
        self.description_input = QLineEdit(self)

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_course)

        layout = QFormLayout()
        layout.addRow('Название курса:', self.name_input)
        layout.addRow('Описание курса:', self.description_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_course(self):
        name = self.name_input.text()
        description = self.description_input.text()

        if name and description:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO courses (name, description) VALUES (%s, %s)",
                           (name, description))
            conn.commit()
            conn.close()
            self.accept()

# Диалог для просмотра студентов
class ViewStudentsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Просмотр студентов')
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(students))
        for row, student in enumerate(students):
            self.table.setItem(row, 0, QTableWidgetItem(str(student[0])))
            self.table.setItem(row, 1, QTableWidgetItem(student[1]))
            self.table.setItem(row, 2, QTableWidgetItem(student[2]))

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

# Диалог для просмотра курсов
class ViewCoursesDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Просмотр курсов')
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Описание'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(courses))
        for row, course in enumerate(courses):
            self.table.setItem(row, 0, QTableWidgetItem(str(course[0])))
            self.table.setItem(row, 1, QTableWidgetItem(course[1]))
            self.table.setItem(row, 2, QTableWidgetItem(course[2]))

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

# Диалог для учета посещаемости
class MarkAttendanceDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Учет посещаемости')
        self.setGeometry(100, 100, 300, 150)

        self.student_combo = QComboBox(self)
        self.course_combo = QComboBox(self)

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(['present', 'absent'])

        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_attendance)

        # Получение студентов и курсов из базы данных
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        self.student_combo.addItems([f"{s[1]} {s[2]}" for s in students])

        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        self.course_combo.addItems([course[1] for course in courses])

        layout = QFormLayout()
        layout.addRow('Студент:', self.student_combo)
        layout.addRow('Курс:', self.course_combo)
        layout.addRow('Статус:', self.status_combo)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_attendance(self):
        student_id = self.student_combo.currentIndex() + 1
        course_id = self.course_combo.currentIndex() + 1
        status = self.status_combo.currentText()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO attendance (student_id, course_id, status) VALUES (%s, %s, %s)",
                       (student_id, course_id, status))
        conn.commit()
        conn.close()
        self.accept()


# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
