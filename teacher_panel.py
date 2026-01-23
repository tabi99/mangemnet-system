from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QTabWidget, QFrame,
    QComboBox, QCheckBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QLinearGradient, QBrush
from PyQt5.QtCore import Qt, QDate

from student_panel import StudentPanel
from database import get_db, get_all_classes, get_students_by_class


# ---------------- GRADIENT LABEL ----------------
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

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor("#3498db"))
        self.setGraphicsEffect(shadow)

        gradient = QLinearGradient(0, 0, 0, 50)
        gradient.setColorAt(0, QColor("#3498db"))
        gradient.setColorAt(1, QColor("#9b59b6"))
        palette = self.palette()
        palette.setBrush(QPalette.WindowText, QBrush(gradient))
        self.setPalette(palette)


# ---------------- TEACHER PANEL ----------------
class TeacherPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Dashboard")
        self.resize(950, 720)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        main_layout.addWidget(GradientLabel("Teacher Dashboard - Student Overview"))

        # -------- CLASS / STUDENT BAR --------
        bar = QFrame()
        bar.setStyleSheet("background:white; border-radius:15px;")
        bar_layout = QHBoxLayout(bar)

        bar_layout.addWidget(QLabel("Select Class:"))
        self.class_combo = QComboBox()
        self.class_combo.addItem("Select Class")
        self.class_combo.addItems(get_all_classes())
        self.class_combo.currentIndexChanged.connect(self.load_students_by_class)
        bar_layout.addWidget(self.class_combo)

        bar_layout.addWidget(QLabel("Select Student:"))
        self.student_combo = QComboBox()
        bar_layout.addWidget(self.student_combo)

        open_btn = QPushButton("Open Dashboard")
        open_btn.setFont(QFont("Arial", 12, QFont.Bold))
        open_btn.setStyleSheet("""
            QPushButton {
                background-color:#3498db;
                color:white;
                border-radius:10px;
                padding:5px 15px;
            }
            QPushButton:hover {
                background-color:#2980b9;
            }
        """)
        open_btn.clicked.connect(self.open_student_panel)
        bar_layout.addWidget(open_btn)
        
       
        main_layout.addWidget(bar)

        # -------- TABS --------
        self.tabs = QTabWidget()
        self.tabs.addTab(self.results_tab(), "Results")
        self.tabs.addTab(self.attendance_tab(), "Attendance")
        main_layout.addWidget(self.tabs)

        # -------- BACKGROUND --------
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ecf0f1"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    # ================= CLASS → STUDENT =================
    def load_students_by_class(self):
        cls = self.class_combo.currentText()

        self.student_combo.clear()
        if hasattr(self, "r_student_combo"):
            self.r_student_combo.clear()
        if hasattr(self, "a_student_combo"):
            self.a_student_combo.clear()

        if cls == "Select Class":
            return

        students = get_students_by_class(cls)

        self.student_combo.addItems(students)

        if hasattr(self, "r_student_combo"):
            self.r_student_combo.addItems(students)

        if hasattr(self, "a_student_combo"):
            self.a_student_combo.addItems(students)

    # ================= RESULTS TAB =================
    def results_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        card = QFrame()
        card.setStyleSheet("background:white; border-radius:10px;")
        card_layout = QVBoxLayout(card)

        form = QHBoxLayout()

        self.r_student_combo = QComboBox()
        self.r_student_combo.currentIndexChanged.connect(self.on_result_student_change)

        self.r_subject = QComboBox()
        self.r_subject.addItems([
            "English","Urdu","Isl","PST","Maths",
            "Physics","Chemistry","Computer","Economics","H.P.E"
        ])

        self.r_marks = QLineEdit()
        self.r_marks.setPlaceholderText("Marks")

        self.r_group = QComboBox()

        add = QPushButton("Add")
        add.clicked.connect(self.add_result)

        form.addWidget(self.r_student_combo)
        form.addWidget(self.r_subject)
        form.addWidget(self.r_marks)
        form.addWidget(self.r_group)
        form.addWidget(add)

        self.result_table = QTableWidget(0, 5)
        self.result_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Subject", "Marks", "Group"]
        )

        card_layout.addLayout(form)
        card_layout.addWidget(self.result_table)
        layout.addWidget(card)

        return tab

    def on_result_student_change(self):
        name = self.r_student_combo.currentText()
        if not name:
            return

        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT class, `student_group` FROM students WHERE name=?", (name,))
        row = cur.fetchone()
        con.close()

        if row:
            self.r_group.clear()
            self.r_group.addItem(f"{row[0]} - {row[1]}")

    def add_result(self):
        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO results (student_name, subject, marks, student_group) VALUES (?,?,?,?)",
            (
                self.r_student_combo.currentText(),
                self.r_subject.currentText(),
                self.r_marks.text(),
                self.r_group.currentText()
            )
        )
        con.commit()
        con.close()

    # ================= ATTENDANCE TAB =================
    def attendance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        card = QFrame()
        card.setStyleSheet("background:white; border-radius:10px;")
        card_layout = QVBoxLayout(card)

        form = QHBoxLayout()

        self.a_student_combo = QComboBox()
        self.a_date = QLineEdit(QDate.currentDate().toString("yyyy-MM-dd"))
        self.a_present = QCheckBox("Present")

        add = QPushButton("Add")

        form.addWidget(self.a_student_combo)
        form.addWidget(self.a_date)
        form.addWidget(self.a_present)
        form.addWidget(add)

        self.att_table = QTableWidget(0, 4)
        self.att_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Date", "Status"]
        )

        card_layout.addLayout(form)
        card_layout.addWidget(self.att_table)
        layout.addWidget(card)

        return tab

    # ================= OPEN STUDENT =================
    def open_student_panel(self):
        name = self.student_combo.currentText()
        if name:
            self.student_dashboard = StudentPanel(name)
            self.student_dashboard.show()
