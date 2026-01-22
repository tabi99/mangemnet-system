# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
# from database import get_all_results
# from charts import ChartCanvas

# class TeacherPanel(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Teacher Dashboard")
#         self.resize(800,600)

#         layout = QVBoxLayout(self)
#         title = QLabel("All Students Performance")
#         layout.addWidget(title)

#         chart = ChartCanvas()
#         layout.addWidget(chart)

#         data = get_all_results()
#         students = {}
#         for name, subject, marks in data:
#             students[name] = students.get(name, 0) + int(marks)

#         chart.bar_chart(
#             list(students.keys()),
#             list(students.values()),
#             "Total Marks of Students"
#         )

# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
# from PyQt5.QtGui import QFont, QColor, QPalette
# from PyQt5.QtCore import Qt
# from database import get_all_results
# from charts import ChartCanvas

# class TeacherPanel(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Teacher Dashboard")
#         self.resize(900, 700)

#         # Overall layout
#         layout = QVBoxLayout(self)
#         layout.setSpacing(15)
#         layout.setContentsMargins(20, 20, 20, 20)

#         # Title
#         title = QLabel("Students Performance Overview")
#         title.setFont(QFont("Arial", 22, QFont.Bold))
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("color: #2c3e50;")
#         layout.addWidget(title)

#         # Chart
#         chart = ChartCanvas()
#         layout.addWidget(chart, stretch=2)

#         # Fetch data
#         data = get_all_results()  # [(name, subject, marks, class/group)]
#         students = {}
#         details = {}
#         for name, subject, marks, class_group in data:
#             students[name] = students.get(name, 0) + int(marks)
#             details[name] = class_group  # Save class/group info

#         # Chart with colors
#         colors = ["#3498db", "#e74c3c", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c"]
#         chart.bar_chart(
#             list(students.keys()),
#             list(students.values()),
#             "Total Marks of Students",
#             colors=colors
#         )

#         # Students cards below chart
#         cards_layout = QHBoxLayout()
#         cards_layout.setSpacing(15)

#         for i, (name, total) in enumerate(students.items()):
#             card = QFrame()
#             card.setFixedSize(150, 120)
#             card.setStyleSheet(f"""
#                 QFrame {{
#                     background-color: {colors[i % len(colors)]};
#                     border-radius: 15px;
#                 }}
#                 QLabel {{
#                     color: white;
#                 }}
#             """)
#             v = QVBoxLayout(card)
#             v.setAlignment(Qt.AlignCenter)

#             lbl_name = QLabel(name)
#             lbl_name.setFont(QFont("Arial", 12, QFont.Bold))
#             lbl_name.setAlignment(Qt.AlignCenter)

#             lbl_marks = QLabel(f"{total} Marks")
#             lbl_marks.setFont(QFont("Arial", 14, QFont.Bold))
#             lbl_marks.setAlignment(Qt.AlignCenter)

#             lbl_class = QLabel(f"Class: {details[name]}")
#             lbl_class.setFont(QFont("Arial", 10))
#             lbl_class.setAlignment(Qt.AlignCenter)

#             v.addWidget(lbl_name)
#             v.addWidget(lbl_marks)
#             v.addWidget(lbl_class)

#             cards_layout.addWidget(card)

#         layout.addLayout(cards_layout, stretch=1)

#         # Set overall background
#         palette = self.palette()
#         palette.setColor(QPalette.Window, QColor("#ecf0f1"))
#         self.setPalette(palette)
#         self.setAutoFillBackground(True)


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from matplotlib.pyplot import title
from student_panel import StudentPanel
from database import get_all_students, get_all_results
from charts import ChartCanvas
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
from PyQt5.QtCore import Qt

# Gradient label class
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

class TeacherPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Dashboard")
        self.resize(900, 700)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = GradientLabel("Teacher Dashboard - Student Overview")
        main_layout.addWidget(title)

        # Dropdown to select student
        select_layout = QHBoxLayout()
        lbl = QLabel("Select Student:")
        lbl.setFont(QFont("Arial", 14))
        select_layout.addWidget(lbl)

        self.student_combo = QComboBox()
        students = get_all_students()  # returns list of student names from DB
        self.student_combo.addItems(students)
        self.student_combo.setFont(QFont("Arial", 12))
        select_layout.addWidget(self.student_combo)

        btn = QPushButton("Open Dashboard")
        btn.setFont(QFont("Arial", 12, QFont.Bold))
        btn.setStyleSheet("""
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
        btn.clicked.connect(self.open_student_panel)
        select_layout.addWidget(btn)

        main_layout.addLayout(select_layout)

        # Optional: Overall chart (all students total marks)
        chart_card = QFrame()
        chart_card.setStyleSheet("QFrame {background:white; border-radius:15px;}")
        chart_layout = QVBoxLayout(chart_card)

        chart = ChartCanvas()
        chart_layout.addWidget(chart)

        # Aggregate all students marks
        data = get_all_results()  # [(name, subject, marks, group_name)]
        students_marks = {}
        for name, subject, marks, group_name in data:
            students_marks[name] = students_marks.get(name, 0) + int(marks)

        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c"]
        chart.bar_chart(list(students_marks.keys()), list(students_marks.values()), "Total Marks of Students", colors=colors)

        main_layout.addWidget(chart_card)

        # Set background
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ecf0f1"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def open_student_panel(self):
        student_name = self.student_combo.currentText()
        if student_name:
            self.student_dashboard = StudentPanel(student_name)
            self.student_dashboard.show()
