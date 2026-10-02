import sqlite3
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'super_secret_placement_key'

DB_NAME = 'placement_system.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Fetch counts
    total_students = cursor.execute("SELECT COUNT(*) FROM STUDENT").fetchone()[0] or 0
    total_companies = cursor.execute("SELECT COUNT(*) FROM COMPANY").fetchone()[0] or 0
    total_jobs = cursor.execute("SELECT COUNT(*) FROM JOB").fetchone()[0] or 0
    total_offers = cursor.execute("SELECT COUNT(*) FROM OFFER").fetchone()[0] or 0
    
    # 2. Query offers via APPLICATION join
    placed_query = """
        SELECT s.name, s.student_code, c.company_name, j.job_title AS role, j.package_lpa AS package
        FROM OFFER o
        JOIN APPLICATION a ON o.application_id = a.application_id
        JOIN STUDENT s ON a.student_id = s.student_id
        JOIN JOB j ON a.job_id = j.job_id
        JOIN COMPANY c ON j.company_id = c.company_id
    """
    
    try:
        placed_students = cursor.execute(placed_query).fetchall()
    except sqlite3.OperationalError:
        # Direct query if OFFER table directly references student_id & job_id
        placed_query_direct = """
            SELECT s.name, s.student_code, c.company_name, j.job_title AS role, j.package_lpa AS package
            FROM APPLICATION a
            JOIN STUDENT s ON a.student_id = s.student_id
            JOIN JOB j ON a.job_id = j.job_id
            JOIN COMPANY c ON j.company_id = c.company_id
            LIMIT 10
        """
        placed_students = cursor.execute(placed_query_direct).fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        total_students=total_students,
        total_companies=total_companies,
        total_jobs=total_jobs,
        total_offers=total_offers,
        placed_students=placed_students
    )

@app.route('/students')
def students():
    conn = get_db_connection()
    students_list = conn.execute("SELECT * FROM STUDENT").fetchall()
    conn.close()
    return render_template('students.html', students=students_list)

@app.route('/jobs')
def jobs():
    conn = get_db_connection()
    drives_query = """
        SELECT j.job_id, c.company_name, j.job_title AS role, j.package_lpa AS package
        FROM JOB j
        JOIN COMPANY c ON j.company_id = c.company_id
    """
    drives = conn.execute(drives_query).fetchall()
    students_list = conn.execute("SELECT student_id, name FROM STUDENT").fetchall()
    conn.close()
    return render_template('jobs.html', drives=drives, students=students_list)

if __name__ == '__main__':
    app.run(debug=True)