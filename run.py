# Advanced School Management System - VIP Version
import sys, sqlite3, hashlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QTabWidget, QFrame, QMessageBox, QComboBox, QCheckBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QDate
from teacher_panel import TeacherPanel
from student_panel import StudentPanel
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
from PyQt5.QtCore import Qt

DB_NAME = "school.db"

# -------- DATABASE --------
def get_db(): return sqlite3.connect(DB_NAME)
def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()

def init_db():
    con = get_db(); cur = con.cursor()
    con = get_db()
    cur = con.cursor()

   
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE, password TEXT, role TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, class TEXT , student_group TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, subject TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, subject TEXT, marks TEXT, student_group TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS fees (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, amount TEXT, status TEXT)""")
    # cur.execute("DROP TABLE IF EXISTS attendance")
    # cur.execute("""CREATE TABLE attendance (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     student_name TEXT,
    #     date TEXT,
    #     status TEXT)""") 
    cur.execute("""CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, date TEXT, status TEXT)""")
    if not cur.execute("SELECT * FROM users WHERE username='admin'").fetchone():
        cur.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                    ("admin", hash_password("admin123"), "admin"))
    con.commit(); con.close()

# -------- GLOBAL STYLE --------
APP_STYLE = """
QWidget {background:#f4f6f8; font-family: Arial; font-size:13px;}
QLineEdit, QComboBox {padding:8px; border-radius:6px; border:1px solid #ccc;}
QPushButton {padding:8px 14px; border-radius:6px; color:white; font-weight:bold;}
QPushButton#add {background:#27ae60;}
QPushButton#update {background:#f2994a;}
QPushButton#delete {background:#eb5757;}
QPushButton:hover {opacity:0.85;}
QTableWidget {background:white; border-radius:6px;}
QHeaderView::section {background:#2f80ed; color:white; padding:6px;}
"""
class GradientLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setFont(QFont("Segoe UI", 26, QFont.Bold))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                border-radius: 12px;
                padding: 15px;
                border: 2px solid #2980b9;
            }
        """)

        # Drop shadow / glow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0,0)
        shadow.setColor(QColor("#3498db"))  # glow color
        self.setGraphicsEffect(shadow)

        # Gradient text using QPalette
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#3498db"))  # Top color
        gradient.setColorAt(1, QColor("#9b59b6"))  # Bottom color
        brush = QBrush(gradient)
        palette.setBrush(QPalette.WindowText, brush)
        self.setPalette(palette)
# -------- LOGIN --------
class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setFixedSize(800, 500)
        self.setStyleSheet("background:#eaf0f6; font-family:Arial;")

        main_layout = QHBoxLayout(self)
        card = QFrame(); card.setFixedSize(350, 420)
        card.setStyleSheet("background:white; border-radius:12px;")
        layout = QVBoxLayout(card); layout.setAlignment(Qt.AlignCenter); layout.setSpacing(15)

        # Logo
        logo = QLabel(); logo.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("icons/download.jfif")  # put your logo
        logo.setPixmap(pixmap.scaled(100,100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Title
        title = QLabel("F.G Girls Inter Collage Login"); title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:20px; font-weight:bold; color:#2f80ed;")

        # Inputs
        self.user = QLineEdit(); self.user.setPlaceholderText("Username")
        self.pwd = QLineEdit(); self.pwd.setPlaceholderText("Password"); self.pwd.setEchoMode(QLineEdit.Password)
        self.user.setStyleSheet(self.input_style()); self.pwd.setStyleSheet(self.input_style())

        # Button
        btn = QPushButton("Login"); btn.setFixedHeight(40)
        btn.setStyleSheet("background:#2f80ed;color:white;font-size:14px;border-radius:8px;")
        btn.clicked.connect(self.login)

        layout.addWidget(logo); layout.addWidget(title)
        layout.addWidget(self.user); layout.addWidget(self.pwd)
        layout.addWidget(btn)
        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        
     
    def input_style(self):
        return "QLineEdit {padding:10px; border:1px solid #ccc; border-radius:8px; font-size:13px;}"
    
    def login(self):
        con = get_db(); cur = con.cursor()
        cur.execute("SELECT role FROM users WHERE username=? AND password=?",
                    (self.user.text(), hash_password(self.pwd.text())))
        row = cur.fetchone(); con.close()
        if not row: QMessageBox.warning(self,"Error","Invalid login"); return
        role = row[0]; self.hide()
        if role == "admin":
            self.win = AdminPanel()

        elif role == "teacher":
            self.win = TeacherPanel()

        elif role == "student":
            # username ko student name assume kar rahe hain
            selected_student = self.user.text()
            self.win = StudentPanel(selected_student)

        self.win.show()
# -------- ADMIN PANEL (VIP) --------
class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.resize(1100,600)
        self.setStyleSheet(APP_STYLE)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        title = GradientLabel("Admin Dashboard")
        main_layout.addWidget(title)

        # 🔷 HEADER
        header = QLabel("Admin Dashboard")
        header.setStyleSheet("font-size:22px; font-weight:bold; color:#2f80ed;")
        main_layout.addWidget(header)

        # 🔷 DASHBOARD COLORED CARDS  ⭐⭐⭐
        main_layout.addWidget(self.dashboard_cards())

        # 🔷 TABS
        self.tabs = QTabWidget()
        self.tabs.addTab(self.students_tab(),"Students")
        self.tabs.addTab(self.teachers_tab(),"Teachers")
        self.tabs.addTab(self.results_tab(),"Results")
        self.tabs.addTab(self.fees_tab(),"Fees")
        self.tabs.addTab(self.attendance_tab(),"Attendance")
        self.tabs.addTab(self.users_tab(),"User Accounts")

        main_layout.addWidget(self.tabs)

        # LOAD DATA
        self.load_students()
        self.load_teachers()
        self.load_results()
        self.load_fees()
        self.load_attendance()
 

    def dashboard_cards(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(15)

 
        layout.addWidget(self.card("Students", self.count("students"), "#00c0ef", 0))
        layout.addWidget(self.card("Teachers", self.count("teachers"), "#f39c12", 1))
        layout.addWidget(self.card("Results", self.count("results"), "#f39c12", 2))
        layout.addWidget(self.card("Fees", self.count("fees"), "#00a65a", 3))
        layout.addWidget(self.card("Attendance", self.count("attendance"), "#00c0ef", 4))
        layout.addWidget(self.card("User Accounts", self.count("users"), "#dd4b39", 5))

        return widget

    def card(self, title, value, color, tab_index):
        frame = QFrame()
        frame.setFixedHeight(110)
        frame.setStyleSheet(f"""
            QFrame {{
                background:{color};
                border-radius:12px;
            }}
            QLabel {{
                color:white;
            }}
        """)

        v = QVBoxLayout(frame)

        num = QLabel(str(value))
        num.setStyleSheet("font-size:28px; font-weight:bold;")

        txt = QLabel(title)
        txt.setStyleSheet("font-size:14px;")

        more = QLabel("More info →")
        more.setAlignment(Qt.AlignRight)
        more.setCursor(Qt.PointingHandCursor)

        def go_to_tab(event):
            self.tabs.setCurrentIndex(tab_index)

        more.mousePressEvent = go_to_tab

        v.addWidget(num)
        v.addWidget(txt)
        v.addStretch()
        v.addWidget(more)

        return frame

    def count(self, table):
        con = get_db()
        cur = con.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        n = cur.fetchone()[0]
        con.close()
        return n

        
    # ------------ User Accounts Tab (Optional) ------------
    def users_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        card = QFrame()
        card.setStyleSheet("background:white; border-radius:10px;")
        card_layout = QVBoxLayout(card)

        title = QLabel("Create Teacher / Student Login")
        title.setStyleSheet("font-size:16px; font-weight:bold;")

        form = QHBoxLayout()

        self.u_username = QLineEdit()
        self.u_username.setPlaceholderText("Username")

        self.u_password = QLineEdit()
        self.u_password.setPlaceholderText("Password")

        self.u_role = QComboBox()
        self.u_role.addItems(["teacher", "student"])

        add = QPushButton("Create User")
        add.setObjectName("add")
        add.clicked.connect(self.add_user)

        form.addWidget(self.u_username)
        form.addWidget(self.u_password)
        form.addWidget(self.u_role)
        form.addWidget(add)

        self.user_table = QTableWidget(0, 4)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Password(Hash)"])
        self.user_table.horizontalHeader().setStretchLastSection(True)

        card_layout.addWidget(title)
        card_layout.addLayout(form)
        card_layout.addWidget(self.user_table)

        layout.addWidget(card)
        self.load_users()

        return tab
    
    # ------------ USER ACCOUNTS CRUD --------

    def add_user(self):
        username = self.u_username.text()
        password = self.u_password.text()
        role = self.u_role.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Fill all fields")
            return

        con = get_db()
        cur = con.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username,password,role) VALUES (?,?,?)",
                (username, hash_password(password), role)
            )
            con.commit()
        except:
            QMessageBox.warning(self, "Error", "Username already exists")
        con.close()

        self.load_users()
        
    # Load users into table
    def load_users(self):
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT id, username, role, password FROM users")
        rows = cur.fetchall()
        con.close()

        self.user_table.setRowCount(0)
        for r in rows:
            row = self.user_table.rowCount()
            self.user_table.insertRow(row)
            for c, v in enumerate(r):
                self.user_table.setItem(row, c, QTableWidgetItem(str(v)))
    # ----- STUDENTS TAB -----
    
    def clear_student_form(self):
        self.s_name.clear()
        self.s_class.setCurrentIndex(0)
        self.s_group.setCurrentIndex(0)

    def clear_teacher_form(self):
        self.t_name.clear()
        self.t_subject.setCurrentIndex(0)
        
    def on_student_change(self):
        student_name = self.r_student_combo.currentText()

        if not student_name or student_name == "Select Student":
            return

        con = get_db()
        cur = con.cursor()

        # students table se class / group uthao
        cur.execute(
            "SELECT student_group FROM students WHERE name=?",
            (student_name,)
        )

        row = cur.fetchone()
        con.close()

        if row:
            group_name = row[0]

            index = self.r_group.findText(group_name)
            if index >= 0:
                self.r_group.setCurrentIndex(index)
            else:
                self.r_group.addItem(group_name)
                self.r_group.setCurrentIndex(self.r_group.count() - 1)
                
    def load_students_into_result_combo(self):
        self.r_student_combo.clear()
        self.r_student_combo.addItem("Select Student")

        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT name FROM students")
        rows = cur.fetchall()
        con.close()

        for r in rows:
            self.r_student_combo.addItem(r[0])

    def students_tab(self):
        tab=QWidget(); layout=QVBoxLayout(tab)
        card=QFrame(); card.setStyleSheet("background:white; border-radius:10px;")
        card_layout=QVBoxLayout(card)
        title=QLabel("Manage Students"); title.setStyleSheet("font-size:16px;font-weight:bold;")

        # Form with buttons
        form=QHBoxLayout(); form.setSpacing(10)
        self.s_name=QLineEdit(); self.s_name.setPlaceholderText("Student Name"); self.s_name.setMinimumWidth(10)
        self.s_class = QComboBox(); self.s_class.addItems(["XI year (F.B)", "XII year (F.B)", "XI year (K.B)", "XII year (K.B)"]); self.s_class.setMinimumWidth(10)

        self.s_group = QComboBox(); self.s_group.addItems(["P.M", "P.E", "ICS", "P.M","ARTS"]); self.s_group.setMinimumWidth(10)

        add=QPushButton("Add"); add.setObjectName("add"); add.setMinimumHeight(10); add.setIcon(QIcon("icons/add.png"))
        add.clicked.connect(self.add_student)
        update=QPushButton("Update"); update.setObjectName("update"); update.setMinimumHeight(35); update.setIcon(QIcon("icons/update.jfif"))
        update.clicked.connect(self.update_student)
        delete=QPushButton("Delete"); delete.setObjectName("delete"); delete.setMinimumHeight(10); delete.setIcon(QIcon("icons/delete.jfif"))
        delete.clicked.connect(self.delete_student)

        form.addWidget(self.s_name); form.addWidget(self.s_class) ;form.addWidget(self.s_group)
        form.addWidget(add); form.addWidget(update); form.addWidget(delete)

        self.student_table=QTableWidget(0,4); self.student_table.setHorizontalHeaderLabels(["ID","Name","Class","Group"])
        self.student_table.horizontalHeader().setStretchLastSection(True)
        self.student_table.cellClicked.connect(self.select_student)

        card_layout.addWidget(title); card_layout.addLayout(form); card_layout.addWidget(self.student_table)
        layout.addWidget(card); return tab

    # ----- TEACHERS TAB -----
    def teachers_tab(self):
        tab=QWidget(); layout=QVBoxLayout(tab)
        card=QFrame(); card.setStyleSheet("background:white; border-radius:10px;")
        card_layout=QVBoxLayout(card)
        title=QLabel("Manage Teachers"); title.setStyleSheet("font-size:16px;font-weight:bold;")

        form=QHBoxLayout(); form.setSpacing(10)
        self.t_name=QLineEdit(); self.t_name.setPlaceholderText("Teacher Name"); self.t_name.setMinimumWidth(150)
        self.t_subject=QComboBox(); self.t_subject.addItems(["English", "Urdu", "Isl", "PST","Maths","Physics","Chemistry","Computer", "Economics","Home Economics", "H.P.E"]); self.t_subject.setMinimumWidth(100)

        add=QPushButton("Add"); add.setObjectName("add"); add.setMinimumHeight(35); add.setIcon(QIcon("icons/add.png"))
        add.clicked.connect(self.add_teacher)
        update=QPushButton("Update"); update.setObjectName("update"); update.setMinimumHeight(35); update.setIcon(QIcon("icons/edit.png"))
        update.clicked.connect(self.update_teacher)
        delete=QPushButton("Delete"); delete.setObjectName("delete"); delete.setMinimumHeight(35); delete.setIcon(QIcon("icons/delete.jfif"))
        delete.clicked.connect(self.delete_teacher)

        form.addWidget(self.t_name); form.addWidget(self.t_subject)
        form.addWidget(add); form.addWidget(update); form.addWidget(delete)

        self.teacher_table=QTableWidget(0,3); self.teacher_table.setHorizontalHeaderLabels(["ID","Name","Subject"])
        self.teacher_table.horizontalHeader().setStretchLastSection(True)
        self.teacher_table.cellClicked.connect(self.select_teacher)

        card_layout.addWidget(title); card_layout.addLayout(form); card_layout.addWidget(self.teacher_table)
        layout.addWidget(card); return tab

    # ----- RESULTS TAB -----
    def results_tab(self):
        tab=QWidget(); layout=QVBoxLayout(tab)
        card=QFrame(); card.setStyleSheet("background:white; border-radius:10px;")
        card_layout=QVBoxLayout(card)
        title=QLabel("Manage Results"); title.setStyleSheet("font-size:16px;font-weight:bold;")

        form=QHBoxLayout(); form.setSpacing(10)
        self.r_student_combo=QComboBox(); self.r_student_combo.setPlaceholderText("Select Student")
        self.r_student_combo.setMinimumWidth(150)
        self.r_student_combo.currentIndexChanged.connect(self.on_student_change)
        self.r_subject=QComboBox(); self.r_subject.addItems(["English", "Urdu", "Isl", "PST","Maths","Physics","Chemistry","Computer", "Economics","Home Economics", "H.P.E"])
        self.r_marks=QLineEdit(); self.r_marks.setPlaceholderText("Marks")
        self.r_group=QComboBox(); self.r_group.setPlaceholderText("Class/Group")

        add=QPushButton("Add"); add.setObjectName("add");add.setMinimumHeight(35); add.setIcon(QIcon("icons/add.png"))
        add.clicked.connect(self.add_result)
        update=QPushButton("Update"); update.setObjectName("update");update.setMinimumHeight(35); update.setIcon(QIcon("icons/update.jfif")); update.clicked.connect(self.update_result)
        delete=QPushButton("Delete"); delete.setObjectName("delete");delete.setMinimumHeight(35); delete.setIcon(QIcon("icons/delete.jfif"));  delete.clicked.connect(self.delete_result)

        form.addWidget(self.r_student_combo); form.addWidget(self.r_subject); form.addWidget(self.r_marks); form.addWidget(self.r_group)
        form.addWidget(add); form.addWidget(update); form.addWidget(delete)

        self.result_table=QTableWidget(0,5); self.result_table.setHorizontalHeaderLabels(["ID","Name","Subject","Marks","Group"])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.cellClicked.connect(self.select_result)

        card_layout.addWidget(title); card_layout.addLayout(form); card_layout.addWidget(self.result_table)
        # layout.addWidget(card); return tab
        layout.addWidget(card)
        self.load_students_into_result_combo()
        return tab
      
    # ----- FEES TAB -----
    def fees_tab(self):
        tab=QWidget(); layout=QVBoxLayout(tab)
        card=QFrame(); card.setStyleSheet("background:white; border-radius:10px;")
        card_layout=QVBoxLayout(card)
        title=QLabel("Manage Fees"); title.setStyleSheet("font-size:16px;font-weight:bold;")

        form=QHBoxLayout(); form.setSpacing(10)
        self.f_student_combo=QComboBox(); self.f_student_combo.setPlaceholderText("Select Student")
        self.f_student_combo.setMinimumWidth(150)
        self.f_amount=QLineEdit(); self.f_amount.setPlaceholderText("Amount")
        self.f_status=QComboBox(); self.f_status.addItems(["Paid", "Unpaid"]); self.f_status.setPlaceholderText("Status")

        add=QPushButton("Add"); add.setObjectName("add"); add.setMinimumHeight(35); add.setIcon(QIcon("icons/add.png")); add.clicked.connect(self.add_fee)
        update=QPushButton("Update"); update.setObjectName("update"); update.setMinimumHeight(35); update.setIcon(QIcon("icons/update.jfif")); update.clicked.connect(self.update_fee)
        delete=QPushButton("Delete"); delete.setObjectName("delete"); delete.setMinimumHeight(35); delete.setIcon(QIcon("icons/delete.jfif")); delete.clicked.connect(self.delete_fee)

        form.addWidget(self.f_student_combo); form.addWidget(self.f_amount); form.addWidget(self.f_status)
        form.addWidget(add); form.addWidget(update); form.addWidget(delete)

        self.fee_table=QTableWidget(0,4); self.fee_table.setHorizontalHeaderLabels(["ID","Name","Amount","Status"])
        self.fee_table.horizontalHeader().setStretchLastSection(True)
        self.fee_table.cellClicked.connect(self.select_fee)

        card_layout.addWidget(title); card_layout.addLayout(form); card_layout.addWidget(self.fee_table)
        layout.addWidget(card); return tab

    # ----- ATTENDANCE TAB -----
    def attendance_tab(self):
        tab=QWidget(); layout=QVBoxLayout(tab)
        card=QFrame(); card.setStyleSheet("background:white; border-radius:10px;")
        card_layout=QVBoxLayout(card)
        title=QLabel("Manage Attendance"); title.setStyleSheet("font-size:16px;font-weight:bold;")

        form=QHBoxLayout(); form.setSpacing(10)
        self.a_student_combo=QComboBox(); self.a_student_combo.setPlaceholderText("Select Student")
        self.a_student_combo.setMinimumWidth(150)
        self.a_date=QLineEdit(); self.a_date.setText(QDate.currentDate().toString("yyyy-MM-dd"))
        self.a_present=QCheckBox("Present"); self.a_present.setStyleSheet("font-size:14px; padding:5px;")

        add=QPushButton("Add"); add.setObjectName("add"); add.setMinimumHeight(35); add.setIcon(QIcon("icons/add.png")); add.clicked.connect(self.add_attendance)
        update=QPushButton("Update"); update.setObjectName("update");update.setMinimumHeight(35); update.setIcon(QIcon("icons/update.jfif"));update.clicked.connect(self.update_attendance)
        delete=QPushButton("Delete"); delete.setObjectName("delete");delete.setMinimumHeight(35); delete.setIcon(QIcon("icons/delete.jfif")); delete.clicked.connect(self.delete_attendance)

        form.addWidget(self.a_student_combo); form.addWidget(self.a_date); form.addWidget(self.a_present)
        form.addWidget(add); form.addWidget(update); form.addWidget(delete)

        self.att_table=QTableWidget(0,4); self.att_table.setHorizontalHeaderLabels(["ID","Name","Date","Status"])
        self.att_table.horizontalHeader().setStretchLastSection(True)
        self.att_table.cellClicked.connect(self.select_attendance)

        card_layout.addWidget(title); card_layout.addLayout(form); card_layout.addWidget(self.att_table)
        layout.addWidget(card); return tab

    # ----- RESULTS CRUD -----
    def add_result(self):
        con=get_db(); cur=con.cursor()
        # cur.execute("INSERT INTO results (student_name,subject,marks,group_name) VALUES (?,?,?,?)",
        #             (self.r_student_combo.currentText(),self.r_subject.currentText(),self.r_marks.text(),self.r_group.text()))
        cur.execute(
            "INSERT INTO results (student_name,subject,marks,student_group) VALUES (?,?,?,?)",
            (
                self.r_student_combo.currentText(),
                self.r_subject.currentText(),
                self.r_marks.text(),
                self.r_group.currentText()
            )
        )
        con.commit(); con.close(); self.load_results()
    def update_result(self):
        if not hasattr(self,"result_id"): return
        con=get_db(); cur=con.cursor()
        cur.execute("UPDATE results SET student_name=?,subject=?,marks=?,group_name=? WHERE id=?",
                    (
            self.r_student_combo.currentText(),
            self.r_subject.currentText(),
            self.r_marks.text(),
            self.r_group.currentText(),
            self.result_id
        ))
        con.commit(); con.close(); self.load_results()
    def delete_result(self):
        if not hasattr(self,"result_id"): return
        con=get_db(); cur=con.cursor()
        cur.execute("DELETE FROM results WHERE id=?",(self.result_id,))
        con.commit(); con.close(); self.load_results()
    def select_result(self,row,col):
        self.result_id=int(self.result_table.item(row,0).text())
        self.r_student_combo.setCurrentText(self.result_table.item(row,1).text())
        self.r_subject.setCurrentText(self.result_table.item(row,2).text())
        self.r_marks.setText(self.result_table.item(row,3).text())
        self.r_group.setCurrentText(self.result_table.item(row,4).text())
    def load_results(self):
        con=get_db(); cur=con.cursor()
        cur.execute("SELECT * FROM results"); rows=cur.fetchall(); con.close()
        self.result_table.setRowCount(0)
        for r in rows:
            row=self.result_table.rowCount(); self.result_table.insertRow(row)
            for c,v in enumerate(r): self.result_table.setItem(row,c,QTableWidgetItem(str(v)))

    # ----- FEES CRUD -----
    def add_fee(self):
        con=get_db(); cur=con.cursor()
        cur.execute("INSERT INTO fees (student_name,amount,status) VALUES (?,?,?)",
                    (self.f_student_combo.currentText(),self.f_amount.text(),self.f_status.currentText()))
        con.commit(); con.close(); self.load_fees()
    def update_fee(self):
        if not hasattr(self,"fee_id"): return
        con=get_db(); cur=con.cursor()
        cur.execute("UPDATE fees SET student_name=?,amount=?,status=? WHERE id=?",
                    (self.f_student_combo.currentText(),self.f_amount.text(),self.f_status.currentText(),self.fee_id))
        con.commit(); con.close(); self.load_fees()
    def delete_fee(self):
        if not hasattr(self,"fee_id"): return
        con=get_db(); cur=con.cursor()
        cur.execute("DELETE FROM fees WHERE id=?",(self.fee_id,))
        con.commit(); con.close(); self.load_fees()
    def select_fee(self,row,col):
        self.fee_id=int(self.fee_table.item(row,0).text())
        self.f_student_combo.setCurrentText(self.fee_table.item(row,1).text())
        self.f_amount.setText(self.fee_table.item(row,2).text())
        self.f_status.setText(self.fee_table.item(row,3).text())
    def load_fees(self):
        con=get_db(); cur=con.cursor()
        cur.execute("SELECT * FROM fees"); rows=cur.fetchall(); con.close()
        self.fee_table.setRowCount(0)
        for r in rows:
            row=self.fee_table.rowCount(); self.fee_table.insertRow(row)
            for c,v in enumerate(r): self.fee_table.setItem(row,c,QTableWidgetItem(str(v)))

    # ----- ATTENDANCE CRUD -----
    def add_attendance(self):
        status = "Present" if self.a_present.isChecked() else "Absent"
        con=get_db(); cur=con.cursor()
        cur.execute("INSERT INTO attendance (student_name,date,status) VALUES (?,?,?)",
                    (self.a_student_combo.currentText(),self.a_date.text(),status))
        con.commit(); con.close(); self.load_attendance()
    def update_attendance(self):
        if not hasattr(self,"att_id"): return
        status = "Present" if self.a_present.isChecked() else "Absent"
        con=get_db(); cur=con.cursor()
        cur.execute("UPDATE attendance SET student_name=?,date=?,status=? WHERE id=?",
                    (self.a_student_combo.currentText(),self.a_date.text(),status,self.att_id))
        con.commit(); con.close(); self.load_attendance()
    def delete_attendance(self):
        if not hasattr(self,"att_id"): return
        con=get_db(); cur=con.cursor()
        cur.execute("DELETE FROM attendance WHERE id=?",(self.att_id,))
        con.commit(); con.close(); self.load_attendance()
    def select_attendance(self,row,col):
        self.att_id=int(self.att_table.item(row,0).text())
        self.a_student_combo.setCurrentText(self.att_table.item(row,1).text())
        self.a_date.setText(self.att_table.item(row,2).text())
        status = self.att_table.item(row,3).text()
        self.a_present.setChecked(True if status=="Present" else False)
    def load_attendance(self):
        con=get_db(); cur=con.cursor()
        cur.execute("SELECT * FROM attendance"); rows=cur.fetchall(); con.close()
        self.att_table.setRowCount(0)
        for r in rows:
            row=self.att_table.rowCount(); self.att_table.insertRow(row)
            for c,v in enumerate(r): self.att_table.setItem(row,c,QTableWidgetItem(str(v)))

    # ----- STUDENT CRUD -----
    def add_student(self):
        con=get_db(); cur=con.cursor()
        cur.execute("INSERT INTO students (name,class,student_group) VALUES (?,?,?)",(self.s_name.text(),self.s_class.currentText(),self.s_group.currentText()))
        con.commit(); con.close(); self.load_students()
        self.clear_student_form()
    def update_student(self):
        if not hasattr(self,"student_id"): return
        con=get_db(); cur=con.cursor()
        # cur.execute("UPDATE students SET name=?,class=?,group=? WHERE id=?",(self.s_name.text(),self.s_class.currentText(),self.s_group.currentText(),self.student_id))
        cur.execute(
            "UPDATE students SET name=?,class=?,student_group=? WHERE id=?",
            (self.s_name.text(),self.s_class.currentText(),self.s_group.currentText(),self.student_id)
        )
        con.commit(); con.close(); self.load_students()
    def delete_student(self):
        if not hasattr(self,"student_id"): return
        con=get_db(); cur=con.cursor()
        cur.execute("DELETE FROM students WHERE id=?",(self.student_id,))
        con.commit(); con.close(); self.load_students()
    def select_student(self,row,col):
        self.student_id=int(self.student_table.item(row,0).text())
        self.s_name.setText(self.student_table.item(row,1).text())
        # self.s_class.setText(self.student_table.item(row,2).text())
        self.s_class.setCurrentText(self.student_table.item(row,2).text())
        self.s_group.setCurrentText(self.student_table.item(row,3).text())
    def load_students(self):
        con=get_db(); cur=con.cursor()
        cur.execute("SELECT * FROM students"); rows=cur.fetchall(); con.close()
        self.student_table.setRowCount(0)
        
        # Clear and update combos
        names = [r[1] for r in rows]
        if hasattr(self, 'r_student_combo'): 
            self.r_student_combo.clear(); self.r_student_combo.addItems(names)
        if hasattr(self, 'f_student_combo'):
            self.f_student_combo.clear(); self.f_student_combo.addItems(names)
        if hasattr(self, 'a_student_combo'):
            self.a_student_combo.clear(); self.a_student_combo.addItems(names)

        for r in rows:
            row=self.student_table.rowCount(); self.student_table.insertRow(row)
            for c,v in enumerate(r): self.student_table.setItem(row,c,QTableWidgetItem(str(v)))

    # ----- TEACHER CRUD -----
    def add_teacher(self):
        con=get_db(); cur=con.cursor()
        cur.execute("INSERT INTO teachers (name,subject) VALUES (?,?)",(self.t_name.text(),self.t_subject.currentText()))
        con.commit(); con.close(); self.load_teachers()
        self.clear_teacher_form()
    def update_teacher(self):
        if not hasattr(self,"teacher_id"): return
        con=get_db(); cur=con.cursor()
        cur.execute("UPDATE teachers SET name=?,subject=? WHERE id=?",(self.t_name.text(),self.t_subject.currentText(),self.teacher_id))
        con.commit(); con.close(); self.load_teachers()
    def delete_teacher(self):
        if not hasattr(self,"teacher_id"): return
        con=get_db(); cur=con.cursor()
        cur.execute("DELETE FROM teachers WHERE id=?",(self.teacher_id,))
        con.commit(); con.close(); self.load_teachers()
    def select_teacher(self,row,col):
        self.teacher_id=int(self.teacher_table.item(row,0).text())
        self.t_name.setText(self.teacher_table.item(row,1).text())
        self.t_subject.setText(self.teacher_table.item(row,2).text())
    def load_teachers(self):
        con=get_db(); cur=con.cursor()
        cur.execute("SELECT * FROM teachers"); rows=cur.fetchall(); con.close()
        self.teacher_table.setRowCount(0)
        for r in rows:
            row=self.teacher_table.rowCount(); self.teacher_table.insertRow(row)
            for c,v in enumerate(r): self.teacher_table.setItem(row,c,QTableWidgetItem(str(v)))


# -------- MAIN --------
if __name__=="__main__":
    init_db()
    app=QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    win=Login()
    win.show()
    sys.exit(app.exec_())
