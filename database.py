import sqlite3

DB_NAME = "school.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def get_all_results():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT student_name, subject, marks, group_name FROM results")
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
    cur.execute("SELECT status, COUNT(*) FROM attendance WHERE student_name=? GROUP BY status", (name,))
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