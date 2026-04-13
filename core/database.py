import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'campus.db')
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'schema.sql')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Read schema
            with open(SCHEMA_PATH, 'r') as f:
                cursor.executescript(f.read())
            
            # Check if departments are seeded
            cursor.execute("SELECT COUNT(*) FROM departments")
            if cursor.fetchone()[0] == 0:
                departments = [
                    ('Housekeeping Department', 'housekeeping@campus.edu', 'Bathroom & Hygiene'),
                    ('Student Affairs / Security Office', 'security@campus.edu', 'Anti-Ragging & Safety'),
                    ('Mess Committee / Warden', 'mess@campus.edu', 'Mess & Food Quality'),
                    ('Academic Office / HOD', 'academic@campus.edu', 'Academic Issues'),
                    ('Campus Maintenance Cell', 'maintenance@campus.edu', 'Infrastructure/Maintenance'),
                    ('General Administration', 'admin@campus.edu', 'Other')
                ]
                cursor.executemany("INSERT INTO departments (name, contact_email, category) VALUES (?, ?, ?)", departments)
            conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")

def insert_problem(id, description, reg_no, email, urgency, image_path=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO problems (id, description, image_path, reg_no, email, urgency, status) VALUES (?, ?, ?, ?, ?, ?, 'Submitted')",
            (id, description, image_path, reg_no, email, urgency)
        )
        conn.commit()

def get_problem(id):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM problems WHERE id = ?", (id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_problems():
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM problems ORDER BY submitted_at DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_problems_by_department(dept):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM problems WHERE department = ? ORDER BY submitted_at DESC", (dept,))
        return [dict(row) for row in cursor.fetchall()]

def update_problem_classification(id, category, confidence, department):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE problems SET category = ?, confidence = ?, department = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (category, confidence, department, id)
        )
        conn.commit()

def update_problem_status(id, status, resolution_note):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE problems SET status = ?, resolution_note = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, resolution_note, id)
        )
        conn.commit()

# Call init_db on import
init_db()
