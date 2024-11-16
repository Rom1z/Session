import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication , QWidget , QLineEdit , QVBoxLayout , QPushButton , QLabel , QFormLayout , \
    QTableWidget , QTableWidgetItem , QDialog , QDialogButtonBox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


# Подключение к базе данных MySQL
def get_db_connection():
    return mysql.connector.connect (
        host='localhost' ,
        user='root' ,
        password='' ,  # Замените на ваш пароль
        database='warehouse_management'
    )


# Функция для авторизации
def authenticate(username , password):
    conn = get_db_connection ()
    cursor = conn.cursor ()
    cursor.execute ( "SELECT role FROM users WHERE username = %s AND password = %s" , (username , password) )
    result = cursor.fetchone ()
    conn.close ()
    if result:
        return result[0]  # Возвращаем роль (manager или warehouse_staff)
    return None


# Класс окна авторизации
class LoginWindow ( QWidget ):
    def __init__(self):
        super ().__init__ ()
        self.setWindowTitle ( 'Авторизация' )
        self.setGeometry ( 100 , 100 , 280 , 120 )

        # Формируем элементы
        layout = QFormLayout ()

        self.username_input = QLineEdit ( self )
        self.password_input = QLineEdit ( self )
        self.password_input.setEchoMode ( QLineEdit.Password )

        login_button = QPushButton ( 'Войти' , self )
        login_button.clicked.connect ( self.login )

        layout.addRow ( 'Имя пользователя' , self.username_input )
        layout.addRow ( 'Пароль' , self.password_input )
        layout.addWidget ( login_button )

        self.setLayout ( layout )

    def login(self):
        username = self.username_input.text ()
        password = self.password_input.text ()

        role = authenticate ( username , password )

        if role:
            self.close ()
            if role == 'manager':
                self.manager_window = ManagerWindow ()
                self.manager_window.show ()
            else:
                self.warehouse_window = WarehouseStaffWindow ()
                self.warehouse_window.show ()
        else:
            print ( "Неверные данные для входа" )


# Класс окна для менеджера
class ManagerWindow ( QWidget ):
    def __init__(self):
        super ().__init__ ()
        self.setWindowTitle ( 'Панель управления менеджера' )
        self.setGeometry ( 100 , 100 , 400 , 300 )

        # Кнопки для добавления/удаления товаров
        layout = QVBoxLayout ()

        self.add_product_button = QPushButton ( 'Добавить товар' , self )
        self.add_product_button.clicked.connect ( self.add_product )

        self.view_products_button = QPushButton ( 'Просмотр товаров' , self )
        self.view_products_button.clicked.connect ( self.view_products )

        self.generate_report_button = QPushButton ( 'Сгенерировать отчет в PDF' , self )
        self.generate_report_button.clicked.connect ( self.generate_report )

        layout.addWidget ( self.add_product_button )
        layout.addWidget ( self.view_products_button )
        layout.addWidget ( self.generate_report_button )

        self.setLayout ( layout )

    def add_product(self):
        # Окно для добавления товара
        self.add_product_dialog = AddProductDialog ()
        self.add_product_dialog.exec_ ()

    def view_products(self):
        # Окно для просмотра товаров
        self.view_products_dialog = ViewProductsDialog ()
        self.view_products_dialog.exec_ ()

    def generate_report(self):
        # Создание отчета в PDF
        conn = get_db_connection ()
        cursor = conn.cursor ()
        cursor.execute ( """
            SELECT products.name, transactions.type, transactions.quantity, transactions.date
            FROM transactions
            JOIN products ON transactions.product_id = products.id
            ORDER BY transactions.date DESC
        """ )
        transactions = cursor.fetchall ()
        conn.close ()

        # Генерация PDF
        pdf_file = "report.pdf"
        c = canvas.Canvas ( pdf_file , pagesize=letter )
        width , height = letter

        c.setFont ( "Helvetica" , 12 )
        c.drawString ( 30 , height - 30 , "Отчет по движению товаров:" )

        y_position = height - 50
        c.drawString ( 30 , y_position , "Товар           Тип         Количество  Дата" )
        y_position -= 20

        for transaction in transactions:
            c.drawString ( 30 , y_position ,
                           f"{transaction[0]}   {transaction[1]}   {transaction[2]}   {transaction[3]}" )
            y_position -= 20
            if y_position < 40:  # Если страница заканчивается, создаем новую страницу
                c.showPage ()
                c.setFont ( "Helvetica" , 12 )
                y_position = height - 30

        c.save ()

        print ( f"Отчет сгенерирован и сохранен как {pdf_file}" )


# Класс окна для сотрудников склада
class WarehouseStaffWindow ( QWidget ):
    def __init__(self):
        super ().__init__ ()
        self.setWindowTitle ( 'Панель сотрудников склада' )
        self.setGeometry ( 100 , 100 , 400 , 300 )

        # Кнопки для просмотра товаров
        layout = QVBoxLayout ()

        self.view_products_button = QPushButton ( 'Просмотр товаров' , self )
        self.view_products_button.clicked.connect ( self.view_products )

        layout.addWidget ( self.view_products_button )

        self.setLayout ( layout )

    def view_products(self):
        self.view_products_dialog = ViewProductsDialog ()
        self.view_products_dialog.exec_ ()


# Диалог для просмотра товаров
class ViewProductsDialog ( QDialog ):
    def __init__(self):
        super ().__init__ ()
        self.setWindowTitle ( 'Просмотр товаров' )
        self.setGeometry ( 100 , 100 , 600 , 400 )

        self.table = QTableWidget ( self )
        self.table.setColumnCount ( 4 )
        self.table.setHorizontalHeaderLabels ( ['ID' , 'Название' , 'Количество' , 'Цена'] )

        conn = get_db_connection ()
        cursor = conn.cursor ()
        cursor.execute ( "SELECT * FROM products" )
        products = cursor.fetchall ()
        conn.close ()

        self.table.setRowCount ( len ( products ) )
        for row , product in enumerate ( products ):
            self.table.setItem ( row , 0 , QTableWidgetItem ( str ( product[0] ) ) )
            self.table.setItem ( row , 1 , QTableWidgetItem ( product[1] ) )
            self.table.setItem ( row , 2 , QTableWidgetItem ( str ( product[2] ) ) )
            self.table.setItem ( row , 3 , QTableWidgetItem ( str ( product[3] ) ) )

        layout = QVBoxLayout ()
        layout.addWidget ( self.table )
        self.setLayout ( layout )


# Диалог для добавления товара
class AddProductDialog ( QDialog ):
    def __init__(self):
        super ().__init__ ()
        self.setWindowTitle ( 'Добавить товар' )
        self.setGeometry ( 100 , 100 , 300 , 150 )

        self.name_input = QLineEdit ( self )
        self.price_input = QLineEdit ( self )
        self.quantity_input = QLineEdit ( self )

        self.save_button = QPushButton ( 'Сохранить' , self )
        self.save_button.clicked.connect ( self.save_product )

        layout = QFormLayout ()
        layout.addRow ( 'Название товара:' , self.name_input )
        layout.addRow ( 'Цена:' , self.price_input )
        layout.addRow ( 'Количество:' , self.quantity_input )
        layout.addWidget ( self.save_button )

        self.setLayout ( layout )

    def save_product(self):
        name = self.name_input.text ()
        price = self.price_input.text ()
        quantity = self.quantity_input.text ()

        if name and price and quantity:
            conn = get_db_connection ()
            cursor = conn.cursor ()
            cursor.execute ( "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)" ,
                             (name , price , quantity) )
            conn.commit ()
            conn.close ()
            self.accept ()


# Запуск приложения
if __name__ == '__main__':
    app = QApplication ( sys.argv )
    window = LoginWindow ()
    window.show ()
    sys.exit ( app.exec_ () )
