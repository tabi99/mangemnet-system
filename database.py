import sqlite3

DB_NAME = "school.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def get_all_results():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT student_name, subject, marks, student_group FROM results")
    data = cur.fetchall()
    con.close()
    return data

def get_student_results(name):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT subject, marks FROM results WHERE student_name=?", (name,))
    data = cur.fetchall()
    con.close()
    return data

def get_student_attendance(name):
    con = get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT 
            s.class,
            s.student_group,
            a.status,
            COUNT(*) 
        FROM attendance a
        JOIN students s ON s.name = a.student_name
        WHERE a.student_name = ?
        GROUP BY a.status
    """, (name,))

    data = cur.fetchall()
    con.close()
    return data


def get_all_students():
    """
    Returns a list of all student names from the database.
    Example: ['Ali Khan', 'Sara Ali', 'Bilal Ahmed']
    """
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT name FROM students")  # assuming your students table has 'name' column
    rows = cur.fetchall()
    con.close()
    # rows is a list of tuples [(name1,), (name2,), ...] → convert to list
    return [r[0] for r in rows]


        
def get_all_classes():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT DISTINCT class FROM students")
    classes = [row[0] for row in cur.fetchall()]
    con.close()
    return classes


def get_students_by_class(class_name):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT name FROM students WHERE class = ?", (class_name,))
    students = [row[0] for row in cur.fetchall()]
    con.close()
    return students


def get_all_results():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT student_name, subject, marks, student_group FROM results")
    data = cur.fetchall()
    con.close()
    return data

def get_student_attendance(name):
    """
    Returns: list of tuples [('Present', 10), ('Absent', 2)]
    """
    con = get_db()
    cur = con.cursor()
    cur.execute("""
        SELECT status, COUNT(*) 
        FROM attendance 
        WHERE student_name=? 
        GROUP BY status
    """, (name,))
    data = cur.fetchall()
    con.close()
    
    # Ensure counts are integers
    return [(status, int(count)) for status, count in data]


def get_student_class_group(name):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT class, `student_group` FROM students WHERE name=?", (name,))
    row = cur.fetchone()
    con.close()
    if row:
        return row[0], row[1]
    return None, None