# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QScrollArea
# from PyQt5.QtGui import QFont, QPalette, QColor
# from PyQt5.QtCore import Qt
# from database import get_student_results, get_student_attendance
# from charts import ChartCanvas

# class StudentPanel(QWidget):
#     def __init__(self, student_name):
#         super().__init__()
#         self.setWindowTitle(f"{student_name} Dashboard")
#         self.resize(900, 600)

#         # Main layout
#         main_layout = QVBoxLayout(self)
#         main_layout.setContentsMargins(20, 20, 20, 20)
#         main_layout.setSpacing(20)

#         # Top Card: Student Info
#         info_card = QFrame()
#         info_card.setStyleSheet("""
#             QFrame {
#                 background-color: #3498db;
#                 border-radius: 15px;
#             }
#             QLabel {
#                 color: white;
#             }
#         """)
#         info_card.setFixedHeight(100)
#         info_layout = QVBoxLayout(info_card)
#         info_layout.setAlignment(Qt.AlignCenter)

#         lbl_name = QLabel(student_name)
#         lbl_name.setFont(QFont("Arial", 20, QFont.Bold))
#         lbl_name.setAlignment(Qt.AlignCenter)

#         # Fetch class/group from attendance table if available
#         att = get_student_attendance(student_name)
 
#         if att:
#             student_class = att[0][0]      # XI year (F.B)
#             student_group = att[0][1]      # P.M
#         else:
#             student_class = "Class N/A"
#             student_group = "Group N/A"
#         lbl_class = QLabel(f"{student_class} - {student_group}")
#         lbl_class.setFont(QFont("Arial", 12))
#         lbl_class.setAlignment(Qt.AlignCenter)

#         info_layout.addWidget(lbl_name)
#         info_layout.addWidget(lbl_class)
#         main_layout.addWidget(info_card)

#         # Scrollable area for charts/cards
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll_content = QWidget()
#         scroll_layout = QHBoxLayout(scroll_content)
#         scroll_layout.setSpacing(20)

#         # Marks Card
#         marks_card = QFrame()
#         marks_card.setStyleSheet("""
#             QFrame {
#                 background:white;
#                 border-radius:15px;
#             }
#             QFrame:hover {
#                 background:#dff9fb;
#             }
#         """)
#         marks_layout = QVBoxLayout(marks_card)

#         chart1 = ChartCanvas()
#         marks_layout.addWidget(chart1)

#         results = get_student_results(student_name)
#         if results:
#             subjects = [r[0] for r in results]
#             marks = [int(r[1]) for r in results]
#             colors = ["#3498db", "#e74c3c", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c"]
#             chart1.bar_chart(subjects, marks, "Marks", colors=colors)

#         # Attendance Card
#         att_card = QFrame()
#         att_card.setStyleSheet("""
#             QFrame {
#                 background:white;
#                 border-radius:15px;
#             }
#             QFrame:hover {
#                 background:#dff9fb;
#             }
#         """)
#         att_layout = QVBoxLayout(att_card)

#         chart2 = ChartCanvas()
#         att_layout.addWidget(chart2)

#         if att:
#             labels = [a[0] for a in att]
#             values = [a[1] for a in att]
#             colors = ["#2ecc71", "#e74c3c"]  # Present/Absent
#             chart2.pie_chart(labels, values, "Attendance", colors=colors)

#         scroll_layout.addWidget(marks_card, stretch=1)
#         scroll_layout.addWidget(att_card, stretch=1)

#         scroll.setWidget(scroll_content)
#         main_layout.addWidget(scroll)

#         # Set overall background
#         palette = self.palette()
#         palette.setColor(QPalette.Window, QColor("#ecf0f1"))
#         self.setPalette(palette)
#         self.setAutoFillBackground(True)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QScrollArea
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from charts import ChartCanvas
from database import get_student_results, get_student_attendance, get_student_class_group

class StudentPanel(QWidget):
    def __init__(self, student_name):
        super().__init__()
        self.setWindowTitle(f"{student_name} Dashboard")
        self.resize(900, 600)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ----------------- Top Card: Student Info -----------------
        info_card = QFrame()
        info_card.setStyleSheet("""
            QFrame {
                background-color: #3498db;
                border-radius: 15px;
            }
            QLabel {
                color: white;
            }
        """)
        info_card.setFixedHeight(100)
        info_layout = QVBoxLayout(info_card)
        info_layout.setAlignment(Qt.AlignCenter)

        lbl_name = QLabel(student_name)
        lbl_name.setFont(QFont("Arial", 20, QFont.Bold))
        lbl_name.setAlignment(Qt.AlignCenter)

        # Fetch class/group from students table
        student_class, student_group = get_student_class_group(student_name)
        if not student_class:
            student_class = "Class N/A"
        if not student_group:
            student_group = "Group N/A"

        lbl_class = QLabel(f"{student_class} - {student_group}")
        lbl_class.setFont(QFont("Arial", 12))
        lbl_class.setAlignment(Qt.AlignCenter)

        info_layout.addWidget(lbl_name)
        info_layout.addWidget(lbl_class)
        main_layout.addWidget(info_card)

        # ----------------- Scrollable Area -----------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)

        # ----------------- Marks Card -----------------
        marks_card = QFrame()
        marks_card.setStyleSheet("""
            QFrame {
                background:white;
                border-radius:15px;
            }
            QFrame:hover {
                background:#dff9fb;
            }
        """)
        marks_layout = QVBoxLayout(marks_card)

        chart1 = ChartCanvas()
        marks_layout.addWidget(chart1)

        results = get_student_results(student_name)
        if results:
            subjects = [r[0] for r in results]
            marks = [int(r[1]) for r in results]
            colors = ["#3498db", "#e74c3c", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c"]
            chart1.bar_chart(subjects, marks, "Marks", colors=colors)

        # ----------------- Attendance Card -----------------
        att_card = QFrame()
        att_card.setStyleSheet("""
            QFrame {
                background:white;
                border-radius:15px;
            }
            QFrame:hover {
                background:#dff9fb;
            }
        """)
        att_layout = QVBoxLayout(att_card)

        chart2 = ChartCanvas()
        att_layout.addWidget(chart2)

        att = get_student_attendance(student_name)
        if att:
            labels = [a[0] for a in att]   # e.g., "Present", "Absent"
            values = [int(a[1]) for a in att]  # numeric count
            colors = ["#2ecc71", "#e74c3c"]  # green/red
            chart2.pie_chart(labels, values, "Attendance", colors=colors)

        # ----------------- Add cards to scroll layout -----------------
        scroll_layout.addWidget(marks_card, stretch=1)
        scroll_layout.addWidget(att_card, stretch=1)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # ----------------- Background -----------------
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ecf0f1"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
