import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'super_secret_placement_key'  # Required for sessions and flash alerts

# Database Connection Helper
def get_db_connection():
    conn = sqlite3.connect('placement_system.db')
    conn.row_factory = sqlite3.Row  # Enables dict-like row access
    return conn

# ----------------------------------------------------
# AUTO-INITIALIZE DATABASE & FIX COMPANY PASSWORDS
# ----------------------------------------------------
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ensure USERS and COMPANY tables exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS COMPANY (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            company_name TEXT NOT NULL,
            industry TEXT,
            contact_email TEXT,
            location TEXT,
            FOREIGN KEY (user_id) REFERENCES USERS(user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JOB (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            job_title TEXT NOT NULL,
            job_description TEXT,
            package_lpa REAL,
            drive_date TEXT,
            FOREIGN KEY (company_id) REFERENCES COMPANY(company_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JOB_ELIGIBILITY (
            eligibility_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            min_cgpa REAL DEFAULT 0.0,
            max_backlogs_allowed INTEGER DEFAULT 0,
            FOREIGN KEY (job_id) REFERENCES JOB(job_id)
        )
    ''')

    # Check if recruiter6 exists; if not, create a guaranteed test company and user
    test_company_email = 'recruiter6@corporate.com'
    existing_user = cursor.execute('SELECT user_id FROM USERS WHERE LOWER(email) = LOWER(?)', (test_company_email,)).fetchone()
    
    if not existing_user:
        cursor.execute('INSERT INTO USERS (email, password_hash, role) VALUES (?, ?, ?)', 
                       (test_company_email, 'companypassword', 'COMPANY'))
        new_user_id = cursor.lastrowid
        cursor.execute('INSERT INTO COMPANY (user_id, company_name, industry, contact_email, location) VALUES (?, ?, ?, ?, ?)',
                       (new_user_id, 'Google', 'Software Product', test_company_email, 'Hyderabad'))
    else:
        # Ensure password is correct
        cursor.execute("UPDATE USERS SET password_hash = 'companypassword' WHERE LOWER(email) = LOWER(?)", (test_company_email,))

    # Globally normalize all company passwords to 'companypassword'
    cursor.execute("UPDATE USERS SET password_hash = 'companypassword' WHERE UPPER(role) = 'COMPANY'")
    
    conn.commit()
    conn.close()

init_db()
# ----------------------------------------------------
# HOME / INDEX ROUTE (Supports both 'index' and 'home' endpoints)
# ----------------------------------------------------
@app.route('/')
@app.route('/home', endpoint='home')
def index():
    if 'role' in session:
        role = session['role']
        if role == 'ADMIN':
            return redirect(url_for('admin_dashboard'))
        elif role == 'STUDENT':
            return redirect(url_for('student_dashboard'))
        elif role == 'COMPANY':
            return redirect(url_for('company_dashboard'))
    return redirect(url_for('login'))

# ----------------------------------------------------
# LOGIN ROUTE
# ----------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        conn = get_db_connection()
        
        # Unified lookup covering USERS email, STUDENT student_code, and COMPANY contact_email
        user = conn.execute('''
            SELECT u.* FROM USERS u
            WHERE (
                LOWER(u.email) = LOWER(?) 
                OR u.user_id IN (SELECT user_id FROM STUDENT WHERE LOWER(student_code) = LOWER(?))
                OR u.user_id IN (SELECT user_id FROM COMPANY WHERE LOWER(contact_email) = LOWER(?))
            )
            AND u.password_hash = ?
        ''', (login_input, login_input, login_input, password)).fetchone()

        conn.close()

        if user:
            session.clear()  # Clear any stale session data
            session['user_id'] = user['user_id']
            session['email'] = user['email']
            session['role'] = str(user['role']).strip().upper()
            
            flash('Login successful!', 'success')
            
            if session['role'] == 'ADMIN':
                return redirect(url_for('admin_dashboard'))
            elif session['role'] == 'STUDENT':
                return redirect(url_for('student_dashboard'))
            elif session['role'] == 'COMPANY':
                return redirect(url_for('company_dashboard'))
            else:
                flash(f'Unrecognized user role: {user["role"]}', 'danger')
        else:
            flash('Invalid email, student code, or password!', 'danger')

    return render_template('login.html')

# ----------------------------------------------------
# LOGOUT ROUTE
# ----------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# ----------------------------------------------------
# ADMIN DASHBOARD
# ----------------------------------------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'ADMIN':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    students_count = conn.execute('SELECT COUNT(*) FROM STUDENT').fetchone()[0]
    companies_count = conn.execute('SELECT COUNT(*) FROM COMPANY').fetchone()[0]
    jobs_count = conn.execute('SELECT COUNT(*) FROM JOB').fetchone()[0]
    applications_count = conn.execute('SELECT COUNT(*) FROM APPLICATION').fetchone()[0] if conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='APPLICATION'").fetchone() else 0
    
    all_students = conn.execute('''
        SELECT s.student_id, s.student_code, s.name, s.email, s.phone,
               p.program_name, a.cgpa, a.active_backlogs
        FROM STUDENT s
        LEFT JOIN PROGRAM p ON s.program_id = p.program_id
        LEFT JOIN ACADEMIC_RECORD a ON s.student_id = a.student_id
        ORDER BY s.student_id ASC
    ''').fetchall()
    
    all_companies = conn.execute('''
        SELECT c.company_id, c.company_name, c.industry, c.contact_email, c.location
        FROM COMPANY c
        ORDER BY c.company_id ASC
    ''').fetchall()

    all_jobs = conn.execute('''
        SELECT j.job_id, j.job_title, j.package_lpa, j.drive_date, 
               c.company_name, e.min_cgpa, e.max_backlogs_allowed
        FROM JOB j 
        JOIN COMPANY c ON j.company_id = c.company_id
        LEFT JOIN JOB_ELIGIBILITY e ON j.job_id = e.job_id
        ORDER BY j.job_id ASC
    ''').fetchall()

    all_applications = []
    if conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='APPLICATION'").fetchone():
        all_applications = conn.execute('''
            SELECT app.app_id, s.name AS student_name, s.student_code, 
                   c.company_name, j.job_title, app.application_date, app.status
            FROM APPLICATION app
            JOIN STUDENT s ON app.student_id = s.student_id
            JOIN JOB j ON app.job_id = j.job_id
            JOIN COMPANY c ON j.company_id = c.company_id
            ORDER BY app.app_id DESC
        ''').fetchall()
    
    conn.close()
    
    stats = {
        'students_count': students_count,
        'companies_count': companies_count,
        'jobs_count': jobs_count,
        'applications_count': applications_count
    }
    
    return render_template(
        'admin_dashboard.html', 
        stats=stats, 
        students=all_students, 
        companies=all_companies, 
        jobs=all_jobs, 
        applications=all_applications
    )

# ----------------------------------------------------
# ADMIN: CLEAR ALL APPLICATIONS
# ----------------------------------------------------
@app.route('/admin/clear_applications', methods=['POST'])
def clear_applications():
    if session.get('role') != 'ADMIN':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM APPLICATION;')
        conn.execute('DELETE FROM sqlite_sequence WHERE name="APPLICATION";')
        conn.commit()
    except Exception:
        pass
    conn.close()
    
    flash('All student applications have been successfully deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

# ----------------------------------------------------
# STUDENT DASHBOARD
# ----------------------------------------------------
@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'STUDENT':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user_id = session.get('user_id')
    
    student = conn.execute('''
        SELECT s.student_id, s.student_code, s.name, s.email, s.phone,
               p.program_name, a.cgpa, a.active_backlogs
        FROM STUDENT s
        LEFT JOIN PROGRAM p ON s.program_id = p.program_id
        LEFT JOIN ACADEMIC_RECORD a ON s.student_id = a.student_id
        WHERE s.user_id = ?
    ''', (user_id,)).fetchone()
    
    available_jobs = conn.execute('''
        SELECT j.job_id, j.job_title, j.package_lpa, j.drive_date, 
               c.company_name, e.min_cgpa, e.max_backlogs_allowed
        FROM JOB j
        JOIN COMPANY c ON j.company_id = c.company_id
        LEFT JOIN JOB_ELIGIBILITY e ON j.job_id = e.job_id
        ORDER BY j.job_id DESC
    ''').fetchall()
    
    applied_jobs = []
    if student and conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='APPLICATION'").fetchone():
        applied_jobs_rows = conn.execute(
            'SELECT job_id FROM APPLICATION WHERE student_id = ?', 
            (student['student_id'],)
        ).fetchall()
        applied_jobs = [row['job_id'] for row in applied_jobs_rows]
        
    conn.close()
    
    return render_template(
        'student_dashboard.html', 
        student=student, 
        available_jobs=available_jobs, 
        applied_job_ids=applied_jobs
    )

# ----------------------------------------------------
# STUDENT: APPLY FOR JOB
# ----------------------------------------------------
@app.route('/student/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if session.get('role') != 'STUDENT':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user_id = session.get('user_id')
    
    student = conn.execute('''
        SELECT s.student_id, a.cgpa, a.active_backlogs 
        FROM STUDENT s
        LEFT JOIN ACADEMIC_RECORD a ON s.student_id = a.student_id
        WHERE s.user_id = ?
    ''', (user_id,)).fetchone()
    
    eligibility = conn.execute('''
        SELECT min_cgpa, max_backlogs_allowed 
        FROM JOB_ELIGIBILITY 
        WHERE job_id = ?
    ''', (job_id,)).fetchone()

    if student and eligibility:
        student_cgpa = student['cgpa'] if student['cgpa'] is not None else 0.0
        student_backlogs = student['active_backlogs'] if student['active_backlogs'] is not None else 0
        
        min_cgpa = eligibility['min_cgpa'] if eligibility['min_cgpa'] is not None else 0.0
        max_backlogs = eligibility['max_backlogs_allowed'] if eligibility['max_backlogs_allowed'] is not None else 99

        if student_cgpa < min_cgpa:
            flash(f'Ineligible to apply. Minimum required CGPA is {min_cgpa}.', 'danger')
        elif student_backlogs > max_backlogs:
            flash(f'Ineligible to apply. Active backlogs exceed allowed limit ({max_backlogs}).', 'danger')
        else:
            try:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS APPLICATION (
                        app_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        job_id INTEGER,
                        application_date TEXT,
                        status TEXT DEFAULT 'APPLIED',
                        FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
                        FOREIGN KEY (job_id) REFERENCES JOB(job_id)
                    )
                ''')
                conn.execute(
                    'INSERT INTO APPLICATION (student_id, job_id, application_date, status) VALUES (?, ?, DATE("now"), "APPLIED")', 
                    (student['student_id'], job_id)
                )
                conn.commit()
                flash('Successfully applied for the placement drive!', 'success')
            except sqlite3.IntegrityError:
                flash('You have already applied for this placement drive.', 'warning')
    else:
        flash('Missing student record or job details.', 'danger')
        
    conn.close()
    return redirect(url_for('student_dashboard'))

# ----------------------------------------------------
# COMPANY DASHBOARD (With Built-in Error Trapping)
# ----------------------------------------------------
# ----------------------------------------------------
# COMPANY DASHBOARD
# ----------------------------------------------------
@app.route('/company/dashboard')
def company_dashboard():
    if session.get('role') != 'COMPANY':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    user_id = session.get('user_id')
    user_email = session.get('email')
    
    company = None
    if user_id:
        company = conn.execute('SELECT * FROM COMPANY WHERE user_id = ?', (user_id,)).fetchone()
    if not company and user_email:
        company = conn.execute('SELECT * FROM COMPANY WHERE LOWER(contact_email) = LOWER(?)', (user_email,)).fetchone()
    
    company_jobs = []
    if company:
        company_jobs = conn.execute('''
            SELECT j.job_id, j.job_title, j.job_description, j.package_lpa, j.drive_date,
                   e.min_cgpa, e.max_backlogs_allowed
            FROM JOB j
            LEFT JOIN JOB_ELIGIBILITY e ON j.job_id = e.job_id
            WHERE j.company_id = ?
            ORDER BY j.job_id DESC
        ''', (company['company_id'],)).fetchall()
        
    conn.close()
    return render_template('company_dashboard.html', company=company, company_jobs=company_jobs)
# ----------------------------------------------------
# COMPANY: POST NEW JOB
# ----------------------------------------------------
@app.route('/company/post_job', methods=['POST'])
def post_job():
    if session.get('role') != 'COMPANY':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
        
    job_title = request.form.get('job_title')
    job_description = request.form.get('job_description')
    package_lpa = request.form.get('package_lpa')
    min_cgpa = request.form.get('min_cgpa', 0.0)
    drive_date = request.form.get('drive_date')
    
    conn = get_db_connection()
    user_id = session.get('user_id')
    user_email = session.get('email')
    
    company = conn.execute('SELECT company_id FROM COMPANY WHERE user_id = ?', (user_id,)).fetchone()
    if not company and user_email:
        company = conn.execute('SELECT company_id FROM COMPANY WHERE LOWER(contact_email) = LOWER(?)', (user_email,)).fetchone()
    
    if company:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO JOB (company_id, job_title, job_description, package_lpa, drive_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (company['company_id'], job_title, job_description, package_lpa, drive_date))
        
        job_id = cur.lastrowid
        cur.execute('INSERT INTO JOB_ELIGIBILITY (job_id, min_cgpa) VALUES (?, ?)', (job_id, min_cgpa))
        
        conn.commit()
        flash('Job drive posted successfully!', 'success')
    else:
        flash('Company profile not found.', 'danger')
        
    conn.close()
    return redirect(url_for('company_dashboard'))

# ----------------------------------------------------
# RUN APPLICATION
# ----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)