# Advanced School Management System (PyQt5 + SQLite)
# Improved UI with Tabs, Styling, and Better Layout

import sys
import sqlite3
import hashlib
from datetime import date
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget,
    QTableWidgetItem, QComboBox, QTabWidget,QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

DB_NAME = "school.db"

# ---------------- DATABASE -----------------

def get_db():
    return sqlite3.connect(DB_NAME)

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def init_db():
    con = get_db()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        class TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username,password,role) VALUES (?,?,?)",
            ("admin", hash_password("admin123"), "admin")
        )

    con.commit()
    con.close()

# ---------------- GLOBAL STYLE -----------------

APP_STYLE = """
QWidget {
    background-color: #f4f6f8;
    font-family: Arial;
    font-size: 13px;
}
QLineEdit, QComboBox {
    padding: 8px;
    border-radius: 6px;
    border: 1px solid #ccc;
}
QPushButton {
    background-color: #2f80ed;
    color: white;
    padding: 8px;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #1c5fc7;
}
QTableWidget {
    background-color: white;
    border-radius: 6px;
}
QHeaderView::section {
    background-color: #2f80ed;
    color: white;
    padding: 6px;
}
"""

# ---------------- LOGIN -----------------

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setFixedSize(800, 500)

        # ===== MAIN BACKGROUND =====
        self.setStyleSheet("""
            QWidget {
                background-color: #eaf0f6;
                font-family: Arial;
            }
        """)

        main_layout = QHBoxLayout(self)

        # ===== CENTER CARD =====
        card = QFrame()
        card.setFixedSize(350, 420)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        # ===== LOGO =====
        logo = QLabel()
        pixmap = QPixmap("download.jfif")   # <-- put your logo file here
        logo.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)

        # ===== TITLE =====
        title = QLabel("School Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:20px; font-weight:bold; color:#2f80ed;")

        # ===== INPUTS =====
        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Password")
        self.pwd.setEchoMode(QLineEdit.Password)

        self.user.setStyleSheet(self.input_style())
        self.pwd.setStyleSheet(self.input_style())

        # ===== BUTTON =====
        btn = QPushButton("Login")
        btn.setFixedHeight(40)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2f80ed;
                color: white;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1c5fc7;
            }
        """)
        btn.clicked.connect(self.login)

        # ===== ADD WIDGETS =====
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(self.user)
        layout.addWidget(self.pwd)
        layout.addWidget(btn)

        main_layout.addWidget(card, alignment=Qt.AlignCenter)

    def input_style(self):
        return """
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 13px;
            }
        """

    def login(self):
        con = get_db()
        cur = con.cursor()
        cur.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (self.user.text(), hash_password(self.pwd.text()))
        )
        row = cur.fetchone()
        con.close()

        if not row:
            QMessageBox.warning(self, "Error", "Invalid login")
            return

        role = row[0]
        self.hide()
        if role == "admin":
            self.win = AdminPanel()
        else:
            self.win = TeacherPanel()
        self.win.show()

# ---------------- ADMIN PANEL -----------------


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.resize(1100, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: Arial;
            }
            QLineEdit {
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
            QPushButton {
                padding: 8px 14px;
                border-radius: 6px;
                color: white;
                font-weight: bold;
            }
            QPushButton#add {
                background-color: #27ae60;
            }
            QPushButton#update {
                background-color: #f2994a;
            }
            QPushButton#delete {
                background-color: #eb5757;
            }
            QPushButton:hover {
                opacity: 0.85;
            }
            QTableWidget {
                background-color: white;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #2f80ed;
                color: white;
                padding: 6px;
                border: none;
            }
        """)

        main_layout = QVBoxLayout(self)

        # ===== HEADER =====
        header = QLabel("Admin Dashboard")
        header.setAlignment(Qt.AlignLeft)
        header.setStyleSheet("font-size:22px; font-weight:bold; color:#2f80ed;")
        main_layout.addWidget(header)

        # ===== TABS =====
        self.tabs = QTabWidget()
        self.tabs.addTab(self.students_tab(), "Students")
        self.tabs.addTab(self.teachers_tab(), "Teachers")

        main_layout.addWidget(self.tabs)

        self.load_students()
        self.load_teachers()

    # ================= STUDENTS TAB =================
    def students_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        card = QFrame()
        card.setStyleSheet("background:white; border-radius:10px;")
        card_layout = QVBoxLayout(card)

        title = QLabel("Manage Students")
        title.setStyleSheet("font-size:16px; font-weight:bold;")

        form = QHBoxLayout()
        self.s_name = QLineEdit()
        self.s_name.setPlaceholderText("Student Name")
        self.s_class = QLineEdit()
        self.s_class.setPlaceholderText("Class")

        add = QPushButton("Add")
        add.setObjectName("add")
        update = QPushButton("Update")
        update.setObjectName("update")
        delete = QPushButton("Delete")
        delete.setObjectName("delete")

        add.clicked.connect(self.add_student)
        update.clicked.connect(self.update_student)
        delete.clicked.connect(self.delete_student)

        form.addWidget(self.s_name)
        form.addWidget(self.s_class)
        form.addWidget(add)
        form.addWidget(update)
        form.addWidget(delete)

        self.student_table = QTableWidget(0, 3)
        self.student_table.setHorizontalHeaderLabels(["ID", "Name", "Class"])
        self.student_table.horizontalHeader().setStretchLastSection(True)
        self.student_table.cellClicked.connect(self.select_student)

        card_layout.addWidget(title)
        card_layout.addLayout(form)
        card_layout.addWidget(self.student_table)

        layout.addWidget(card)
        return tab

    # ================= TEACHERS TAB =================
    def teachers_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        card = QFrame()
        card.setStyleSheet("background:white; border-radius:10px;")
        card_layout = QVBoxLayout(card)

        title = QLabel("Manage Teachers")
        title.setStyleSheet("font-size:16px; font-weight:bold;")

        form = QHBoxLayout()
        self.t_name = QLineEdit()
        self.t_name.setPlaceholderText("Teacher Name")
        self.t_subject = QLineEdit()
        self.t_subject.setPlaceholderText("Subject")

        add = QPushButton("Add")
        add.setObjectName("add")
        update = QPushButton("Update")
        update.setObjectName("update")
        delete = QPushButton("Delete")
        delete.setObjectName("delete")

        add.clicked.connect(self.add_teacher)
        update.clicked.connect(self.update_teacher)
        delete.clicked.connect(self.delete_teacher)

        form.addWidget(self.t_name)
        form.addWidget(self.t_subject)
        form.addWidget(add)
        form.addWidget(update)
        form.addWidget(delete)

        self.teacher_table = QTableWidget(0, 3)
        self.teacher_table.setHorizontalHeaderLabels(["ID", "Name", "Subject"])
        self.teacher_table.horizontalHeader().setStretchLastSection(True)
        self.teacher_table.cellClicked.connect(self.select_teacher)

        card_layout.addWidget(title)
        card_layout.addLayout(form)
        card_layout.addWidget(self.teacher_table)

        layout.addWidget(card)
        return tab

    # -------- STUDENT CRUD --------
    def add_student(self):
        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO students (name,class) VALUES (?,?)",
                    (self.s_name.text(), self.s_class.text()))
        con.commit(); con.close()
        self.load_students()

    def update_student(self):
        if not hasattr(self, 'student_id'): return
        con = get_db(); cur = con.cursor()
        cur.execute("UPDATE students SET name=?, class=? WHERE id=?",
                    (self.s_name.text(), self.s_class.text(), self.student_id))
        con.commit(); con.close()
        self.load_students()

    def delete_student(self):
        if not hasattr(self, 'student_id'): return
        con = get_db(); cur = con.cursor()
        cur.execute("DELETE FROM students WHERE id=?", (self.student_id,))
        con.commit(); con.close()
        self.load_students()

    def select_student(self, row, col):
        self.student_id = int(self.student_table.item(row, 0).text())
        self.s_name.setText(self.student_table.item(row, 1).text())
        self.s_class.setText(self.student_table.item(row, 2).text())

    def load_students(self):
        con = get_db(); cur = con.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall(); con.close()
        self.student_table.setRowCount(0)
        for r in rows:
            row = self.student_table.rowCount()
            self.student_table.insertRow(row)
            for c, v in enumerate(r):
                self.student_table.setItem(row, c, QTableWidgetItem(str(v)))

    # -------- TEACHER CRUD --------
    def add_teacher(self):
        con = get_db(); cur = con.cursor()
        cur.execute("INSERT INTO teachers (name,subject) VALUES (?,?)",
                    (self.t_name.text(), self.t_subject.text()))
        con.commit(); con.close()
        self.load_teachers()

    def update_teacher(self):
        if not hasattr(self, 'teacher_id'): return
        con = get_db(); cur = con.cursor()
        cur.execute("UPDATE teachers SET name=?, subject=? WHERE id=?",
                    (self.t_name.text(), self.t_subject.text(), self.teacher_id))
        con.commit(); con.close()
        self.load_teachers()

    def delete_teacher(self):
        if not hasattr(self, 'teacher_id'): return
        con = get_db(); cur = con.cursor()
        cur.execute("DELETE FROM teachers WHERE id=?", (self.teacher_id,))
        con.commit(); con.close()
        self.load_teachers()

    def select_teacher(self, row, col):
        self.teacher_id = int(self.teacher_table.item(row, 0).text())
        self.t_name.setText(self.teacher_table.item(row, 1).text())
        self.t_subject.setText(self.teacher_table.item(row, 2).text())

    def load_teachers(self):
        con = get_db(); cur = con.cursor()
        cur.execute("SELECT * FROM teachers")
        rows = cur.fetchall(); con.close()
        self.teacher_table.setRowCount(0)
        for r in rows:
            row = self.teacher_table.rowCount()
            self.teacher_table.insertRow(row)
            for c, v in enumerate(r):
                self.teacher_table.setItem(row, c, QTableWidgetItem(str(v)))

# ---------------- MAIN -----------------

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    win = Login()
    win.show()
    sys.exit(app.exec_())
