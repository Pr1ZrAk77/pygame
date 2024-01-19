import sys
import subprocess
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget


class Play1(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/f2.ui', self)
        self.launch.clicked.connect(self.la)

    def la(self):
        if self.lineEdit.text() != '':
            # Устанавливаем соединение с базой данных
            connection = sqlite3.connect('data/my_database.db')
            cursor = connection.cursor()
            # Добавляем нового пользователя
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
            username TEXT NOT NULL,
            level TEXT NOT NULL,
            score INTEGER
            )
            ''')
            cursor.execute('''INSERT INTO Users (username, level, score) VALUES (?, ?, ?)''',
                           (self.lineEdit.text(), '', 0))
            # Сохраняем изменения и закрываем соединение
            connection.commit()
            connection.close()
            with open('data/user.txt', 'w', encoding='utf-8') as text_file:
                text_file.write(self.lineEdit.text())
            with open('data/lev.txt', 'w', encoding='utf-8') as text_file:
                if self.hard.isChecked():
                    text_file.write('хардкор')
                elif self.medi.isChecked():
                    text_file.write('средний')
                elif self.lat.isChecked():
                    text_file.write('лайт')

            subprocess.call("snake.py", shell=True)
            self.close()
        elif self.lineEdit.text() == '':
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Правила игры")
            dlg.setText('Введите игровое имя или выберите уровень')

            button = dlg.exec()


class Records(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/recordsUI.ui', self)

        connection = sqlite3.connect('data/my_database.db')
        cursor = connection.cursor()
        result = cursor.execute('''SELECT username, score FROM Users''').fetchall()
        result = sorted(result, key=lambda x: x[1], reverse=True)[:3]
        s = result[0]
        self.label_5.setText(s[0] + '\t' + str(s[1]))
        s = result[1]
        self.label_6.setText(s[0] + '\t' + str(s[1]))
        s = result[2]
        self.label_7.setText(s[0] + '\t' + str(s[1]))
        connection.close()
        self.Button.clicked.connect(self.toggle_window)
        self.Button.clicked.connect(self.close)

    def toggle_window(self, checked):
        self.pl = MyGame()
        self.pl.show()


class MyGame(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/untitled.ui', self)

        self.play.clicked.connect(self.starts)
        self.rules.clicked.connect(self.dialog)
        self.record.clicked.connect(self.recordes)

    def starts(self):
        self.pl = Play1()
        self.pl.show()
        self.hide()

    def dialog(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Правила игры")
        f = open('data/r.txt', encoding='utf-8')
        dlg.setText(f.read())

        button = dlg.exec()

    def recordes(self):
        self.recor = Records()
        self.recor.show()
        self.hide()


#def custom_excepthook(type, value, traceback):
#    # Custom exception handling code here
#    print("Custom excepthook called")
#
#
## Set the default excepthook to custom_excepthook
#sys.excepthook = custom_excepthook

app = QApplication(sys.argv)
ex = MyGame()
ex.show()
sys.exit(app.exec_())