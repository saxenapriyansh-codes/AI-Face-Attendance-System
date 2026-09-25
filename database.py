import sqlite3
from datetime import date, datetime

DATABASE = "attendance.db"


# -----------------------------------
# Create Database Tables
# -----------------------------------

def create_tables():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            enrollment_no TEXT UNIQUE NOT NULL,
            email TEXT,
            face_data BLOB
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT DEFAULT 'Present',

            FOREIGN KEY (student_id)
            REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------
# Add Student
# -----------------------------------

def add_student(name, enrollment_no, email, face_data=None):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO students
            (name, enrollment_no, email, face_data)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            enrollment_no,
            email,
            face_data
        ))

        conn.commit()

        student_id = cursor.lastrowid

        return True, student_id

    except sqlite3.IntegrityError:

        return False, None

    finally:

        conn.close()


# -----------------------------------
# Get All Students
# -----------------------------------

def get_all_students():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, enrollment_no, email, face_data
        FROM students
    """)

    students = cursor.fetchall()

    conn.close()

    return students


# -----------------------------------
# Get Student By ID
# -----------------------------------

def get_student_by_id(student_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, enrollment_no, email, face_data
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    conn.close()

    return student


# -----------------------------------
# Check Today's Attendance
# -----------------------------------

def attendance_already_marked(student_id):

    today = date.today().isoformat()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM attendance
        WHERE student_id = ?
        AND date = ?
    """, (
        student_id,
        today
    ))

    result = cursor.fetchone()

    conn.close()

    return result is not None


# -----------------------------------
# Mark Attendance
# -----------------------------------

def mark_attendance(student_id):

    # Prevent duplicate attendance
    if attendance_already_marked(student_id):
        return False

    now = datetime.now()

    today = now.date().isoformat()
    current_time = now.strftime("%H:%M:%S")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance
        (student_id, date, time, status)
        VALUES (?, ?, ?, ?)
    """, (
        student_id,
        today,
        current_time,
        "Present"
    ))

    conn.commit()
    conn.close()

    return True


# -----------------------------------
# Get Attendance Records
# -----------------------------------

def get_attendance():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            attendance.id,
            students.name,
            students.enrollment_no,
            students.email,
            attendance.date,
            attendance.time,
            attendance.status

        FROM attendance

        JOIN students
        ON attendance.student_id = students.id

        ORDER BY attendance.date DESC,
                 attendance.time DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records
# -----------------------------------
# Update Student Face Data
# -----------------------------------

def update_face_data(student_id, face_data):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET face_data = ?
        WHERE id = ?
    """, (
        face_data,
        student_id
    ))

    conn.commit()
    conn.close()


# -----------------------------------
# Find Student By Enrollment
# -----------------------------------

def get_student_by_enrollment(enrollment_no):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, enrollment_no, email, face_data
        FROM students
        WHERE enrollment_no = ?
    """, (enrollment_no,))

    student = cursor.fetchone()

    conn.close()

    return student
# -----------------------------------
# Get Attendance For Specific Date
# -----------------------------------

def get_attendance_by_date(selected_date):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            students.id,
            students.name,
            students.enrollment_no,
            students.email,
            attendance.date,
            attendance.time,
            attendance.status

        FROM students

        LEFT JOIN attendance
        ON students.id = attendance.student_id
        AND attendance.date = ?

        ORDER BY students.name
    """, (selected_date,))

    records = cursor.fetchall()

    conn.close()

    return records
# -----------------------------------
# Get Student Attendance By Date Range
# -----------------------------------

def get_student_attendance(
    student_id,
    start_date,
    end_date
):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            date,
            time,
            status
        FROM attendance
        WHERE student_id = ?
        AND date BETWEEN ? AND ?
        ORDER BY date DESC
    """, (
        student_id,
        start_date,
        end_date
    ))

    records = cursor.fetchall()

    conn.close()

    return records
# -----------------------------------
# Delete Student
# -----------------------------------

def delete_student(student_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:

        # Delete attendance records first
        cursor.execute("""
            DELETE FROM attendance
            WHERE student_id = ?
        """, (student_id,))

        # Delete student record
        cursor.execute("""
            DELETE FROM students
            WHERE id = ?
        """, (student_id,))

        conn.commit()

        return True

    except sqlite3.Error:

        conn.rollback()

        return False

    finally:

        conn.close()