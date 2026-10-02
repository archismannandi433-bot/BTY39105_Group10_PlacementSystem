import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

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
    
    total_students = cursor.execute("SELECT COUNT(*) FROM STUDENT").fetchone()[0] or 0
    total_companies = cursor.execute("SELECT COUNT(*) FROM COMPANY").fetchone()[0] or 0
    total_jobs = cursor.execute("SELECT COUNT(*) FROM JOB").fetchone()[0] or 0
    total_offers = cursor.execute("SELECT COUNT(*) FROM OFFER").fetchone()[0] or 0
    
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
    # Joined with PROGRAM and ACADEMIC_RECORD tables
    students_query = """
        SELECT 
            s.student_id,
            s.student_code,
            s.name,
            s.email,
            s.phone,
            p.program_name,
            p.department,
            ar.cgpa,
            ar.active_backlogs
        FROM STUDENT s
        LEFT JOIN PROGRAM p ON s.program_id = p.program_id
        LEFT JOIN ACADEMIC_RECORD ar ON s.student_id = ar.student_id
    """
    students_list = conn.execute(students_query).fetchall()
    conn.close()
    return render_template('students.html', students=students_list)

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    conn = get_db_connection()
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        job_id = request.form.get('job_id')
        if student_id and job_id:
            conn.execute(
                "INSERT INTO APPLICATION (student_id, job_id, status) VALUES (?, ?, 'Applied')",
                (student_id, job_id)
            )
            conn.commit()
            flash('Application submitted successfully!', 'success')
            conn.close()
            return redirect(url_for('jobs'))

    # Joined JOB with COMPANY and JOB_ELIGIBILITY tables
    drives_query = """
        SELECT 
            j.job_id,
            j.job_title AS role,
            j.job_description,
            j.package_lpa AS package,
            j.drive_date,
            c.company_name,
            e.min_cgpa,
            e.max_backlogs_allowed
        FROM JOB j
        JOIN COMPANY c ON j.company_id = c.company_id
        LEFT JOIN JOB_ELIGIBILITY e ON j.job_id = e.job_id
    """
    drives = conn.execute(drives_query).fetchall()
    students_list = conn.execute("SELECT student_id, name FROM STUDENT").fetchall()
    conn.close()
    return render_template('jobs.html', drives=drives, students=students_list)

if __name__ == '__main__':
    app.run(debug=True)