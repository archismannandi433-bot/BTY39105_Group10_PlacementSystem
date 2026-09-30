import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "pbl_placement_secret_key"
DB_NAME = "placement_system.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Drop existing tables
    cursor.executescript('''
        DROP TABLE IF EXISTS OFFER;
        DROP TABLE IF EXISTS APPLICATION;
        DROP TABLE IF EXISTS JOB_ELIGIBILITY;
        DROP TABLE IF EXISTS JOB;
        DROP TABLE IF EXISTS COMPANY;
        DROP TABLE IF EXISTS ACADEMIC_RECORD;
        DROP TABLE IF EXISTS STUDENT;
        DROP TABLE IF EXISTS PROGRAM;
    ''')

    # Create Tables
    cursor.executescript('''
        CREATE TABLE PROGRAM (
            program_id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_name TEXT NOT NULL,
            department TEXT NOT NULL
        );

        CREATE TABLE STUDENT (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            program_id INTEGER,
            FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id) ON DELETE SET NULL
        );

        CREATE TABLE ACADEMIC_RECORD (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER UNIQUE NOT NULL,
            cgpa REAL NOT NULL CHECK(cgpa >= 0.0 AND cgpa <= 10.0),
            active_backlogs INTEGER DEFAULT 0,
            tenth_percentage REAL,
            twelfth_percentage REAL,
            FOREIGN KEY (student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE
        );

        CREATE TABLE COMPANY (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            industry TEXT,
            contact_email TEXT,
            location TEXT
        );

        CREATE TABLE JOB (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            job_title TEXT NOT NULL,
            job_description TEXT,
            package_lpa REAL NOT NULL,
            drive_date DATE,
            FOREIGN KEY (company_id) REFERENCES COMPANY(company_id) ON DELETE CASCADE
        );

        CREATE TABLE JOB_ELIGIBILITY (
            eligibility_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER UNIQUE NOT NULL,
            min_cgpa REAL DEFAULT 6.0,
            max_backlogs_allowed INTEGER DEFAULT 0,
            FOREIGN KEY (job_id) REFERENCES JOB(job_id) ON DELETE CASCADE
        );

        CREATE TABLE APPLICATION (
            app_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            application_date DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'APPLIED' CHECK(status IN ('APPLIED', 'SHORTLISTED', 'REJECTED', 'OFFERED')),
            UNIQUE(student_id, job_id),
            FOREIGN KEY (student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE,
            FOREIGN KEY (job_id) REFERENCES JOB(job_id) ON DELETE CASCADE
        );

        CREATE TABLE OFFER (
            offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_id INTEGER UNIQUE NOT NULL,
            offer_letter_code TEXT UNIQUE NOT NULL,
            offered_salary_lpa REAL NOT NULL,
            joining_date DATE,
            FOREIGN KEY (app_id) REFERENCES APPLICATION(app_id) ON DELETE CASCADE
        );
    ''')

    # Insert Programs
    cursor.executescript('''
        INSERT INTO PROGRAM (program_name, department) VALUES 
        ('B.Tech CSE - Cyber Security', 'CSE'),
        ('B.Tech CSE - Data Science', 'CSE'),
        ('B.Tech CSE - Artificial Intelligence', 'CSE'),
        ('B.Tech ECE - Electronics & Comm', 'ECE'),
        ('BCA - Computer Applications', 'IT');
    ''')

    # Insert 22 Students
    students_data = [
        ('BWU/BCC/25/001', 'Pritam Goldar', 'pritam.g@example.com', '9876543210', 1),
        ('BWU/BCC/25/002', 'Avinava Nandi', 'avinava.n@example.com', '9876543211', 1),
        ('BWU/BCC/25/003', 'Trishita Pal', 'trishita.p@example.com', '9876543212', 2),
        ('BWU/BCC/25/004', 'Aarav Sharma', 'aarav.s@example.com', '9876543213', 3),
        ('BWU/BCC/25/005', 'Ananya Roy', 'ananya.r@example.com', '9876543214', 2),
        ('BWU/BCC/25/006', 'Rohan Das', 'rohan.d@example.com', '9876543215', 1),
        ('BWU/BCC/25/007', 'Sneha Banerjee', 'sneha.b@example.com', '9876543216', 3),
        ('BWU/BCC/25/008', 'Sourav Ganguly', 'sourav.g@example.com', '9876543217', 4),
        ('BWU/BCC/25/009', 'Srinjay Ghosh', 'srinjay.g@example.com', '9876543218', 2),
        ('BWU/BCC/25/010', 'Diya Saha', 'diya.s@example.com', '9876543219', 5),
        ('BWU/BCC/25/011', 'Debanjan Sen', 'debanjan.s@example.com', '9876543220', 1),
        ('BWU/BCC/25/012', 'Subham Mukherjee', 'subham.m@example.com', '9876543221', 3),
        ('BWU/BCC/25/013', 'Pooja Dutta', 'pooja.d@example.com', '9876543222', 2),
        ('BWU/BCC/25/014', 'Arpan Bhattacharya', 'arpan.b@example.com', '9876543223', 4),
        ('BWU/BCC/25/015', 'Riya Bose', 'riya.b@example.com', '9876543224', 5),
        ('BWU/BCC/25/016', 'Koushik Mitra', 'koushik.m@example.com', '9876543225', 1),
        ('BWU/BCC/25/017', 'Tiyasa Kundu', 'tiyasa.k@example.com', '9876543226', 2),
        ('BWU/BCC/25/018', 'Akash Pramanik', 'akash.p@example.com', '9876543227', 3),
        ('BWU/BCC/25/019', 'Megha Chakraborty', 'megha.c@example.com', '9876543228', 4),
        ('BWU/BCC/25/020', 'Sayan Paul', 'sayan.p@example.com', '9876543229', 5),
        ('BWU/BCC/25/021', 'Nisha Agarwal', 'nisha.a@example.com', '9876543230', 1),
        ('BWU/BCC/25/022', 'Rishi Verma', 'rishi.v@example.com', '9876543231', 3)
    ]
    cursor.executemany("INSERT INTO STUDENT (student_code, name, email, phone, program_id) VALUES (?, ?, ?, ?, ?);", students_data)

    # Academic Records corresponding to the 22 students
    academic_data = [
        (1, 8.8, 0, 88.5, 85.0),
        (2, 7.8, 0, 82.0, 79.0),
        (3, 6.2, 1, 75.0, 70.0),
        (4, 9.2, 0, 92.0, 90.0),
        (5, 8.1, 0, 85.0, 84.0),
        (6, 6.8, 2, 72.0, 68.0),
        (7, 8.6, 0, 89.0, 86.5),
        (8, 7.4, 0, 78.0, 76.0),
        (9, 8.9, 0, 91.0, 88.0),
        (10, 6.5, 1, 70.0, 67.0),
        (11, 7.9, 0, 81.0, 80.0),
        (12, 9.5, 0, 96.0, 94.0),
        (13, 8.3, 0, 86.0, 83.0),
        (14, 6.1, 2, 68.0, 65.0),
        (15, 7.2, 0, 76.0, 74.0),
        (16, 8.7, 0, 88.0, 87.0),
        (17, 8.4, 0, 87.0, 85.0),
        (18, 5.9, 1, 65.0, 62.0),
        (19, 7.6, 0, 80.0, 78.0),
        (20, 8.0, 0, 83.0, 81.0),
        (21, 9.1, 0, 93.0, 91.0),
        (22, 6.9, 0, 73.0, 71.0)
    ]
    cursor.executemany("INSERT INTO ACADEMIC_RECORD (student_id, cgpa, active_backlogs, tenth_percentage, twelfth_percentage) VALUES (?, ?, ?, ?, ?);", academic_data)

    # Insert 6 Companies
    cursor.executescript('''
        INSERT INTO COMPANY (company_name, industry, contact_email, location) VALUES 
        ('TCS', 'IT Services', 'hr@tcs.com', 'Kolkata'),
        ('Microsoft', 'Product Development', 'recruitment@microsoft.com', 'Bangalore'),
        ('Cognizant', 'IT & Consulting', 'careers@cognizant.com', 'Kolkata'),
        ('Amazon', 'E-Commerce / Cloud', 'university@amazon.com', 'Hyderabad'),
        ('Wipro', 'IT Services', 'campus@wipro.com', 'Pune'),
        ('Deloitte', 'Financial Consulting', 'graduates@deloitte.com', 'Gurgaon');
    ''')

    # Insert 7 Job Drives
    jobs_data = [
        (1, 'System Engineer', 3.6, '2026-10-15'),
        (2, 'Software Engineer', 14.0, '2026-11-01'),
        (3, 'Programmer Analyst', 4.2, '2026-10-20'),
        (4, 'SDE-1', 18.5, '2026-11-10'),
        (5, 'Project Engineer', 3.8, '2026-10-25'),
        (6, 'Risk Analyst', 7.5, '2026-11-05'),
        (1, 'Digital Software Engineer', 7.0, '2026-10-18')
    ]
    cursor.executemany("INSERT INTO JOB (company_id, job_title, package_lpa, drive_date) VALUES (?, ?, ?, ?);", jobs_data)

    # Insert Job Eligibility Criteria
    eligibility_data = [
        (1, 6.5, 1),
        (2, 8.0, 0),
        (3, 6.0, 1),
        (4, 8.5, 0),
        (5, 6.0, 1),
        (6, 7.0, 0),
        (7, 7.5, 0)
    ]
    cursor.executemany("INSERT INTO JOB_ELIGIBILITY (job_id, min_cgpa, max_backlogs_allowed) VALUES (?, ?, ?);", eligibility_data)

    # Insert Applications
    apps_data = [
        (1, 1, 'OFFERED'),
        (2, 1, 'OFFERED'),
        (4, 2, 'OFFERED'),
        (5, 2, 'OFFERED'),
        (7, 2, 'OFFERED'),
        (9, 4, 'OFFERED'),
        (12, 4, 'OFFERED'),
        (13, 3, 'OFFERED'),
        (16, 6, 'OFFERED'),
        (17, 7, 'OFFERED'),
        (21, 4, 'OFFERED'),
        (1, 2, 'SHORTLISTED'),
        (3, 1, 'APPLIED'),
        (8, 3, 'SHORTLISTED'),
        (11, 5, 'APPLIED'),
        (15, 3, 'APPLIED'),
        (19, 5, 'SHORTLISTED'),
        (20, 6, 'SHORTLISTED'),
        (22, 5, 'APPLIED')
    ]
    cursor.executemany("INSERT INTO APPLICATION (student_id, job_id, status) VALUES (?, ?, ?);", apps_data)

    # Insert 11 Offer Records
    offers_data = [
        (1, 'OFF-TCS-001', 3.6, '2027-06-01'),
        (2, 'OFF-TCS-002', 3.6, '2027-06-01'),
        (3, 'OFF-MSFT-001', 14.0, '2027-07-15'),
        (4, 'OFF-MSFT-002', 14.0, '2027-07-15'),
        (5, 'OFF-MSFT-003', 14.0, '2027-07-15'),
        (6, 'OFF-AMZN-001', 18.5, '2027-08-01'),
        (7, 'OFF-AMZN-002', 18.5, '2027-08-01'),
        (8, 'OFF-CTS-001', 4.2, '2027-06-15'),
        (9, 'OFF-DEL-001', 7.5, '2027-07-01'),
        (10, 'OFF-TCSD-001', 7.0, '2027-06-01'),
        (11, 'OFF-AMZN-003', 18.5, '2027-08-01')
    ]
    cursor.executemany("INSERT INTO OFFER (app_id, offer_letter_code, offered_salary_lpa, joining_date) VALUES (?, ?, ?, ?);", offers_data)

    conn.commit()
    conn.close()

# Routes
@app.route('/')
def dashboard():
    conn = get_db_connection()
    
    total_students = conn.execute('SELECT COUNT(*) FROM STUDENT').fetchone()[0]
    total_companies = conn.execute('SELECT COUNT(*) FROM COMPANY').fetchone()[0]
    total_jobs = conn.execute('SELECT COUNT(*) FROM JOB').fetchone()[0]
    total_offers = conn.execute('SELECT COUNT(*) FROM OFFER').fetchone()[0]

    placed_query = '''
        SELECT s.student_code, s.name, c.company_name, j.job_title, o.offered_salary_lpa, o.offer_letter_code, o.joining_date
        FROM OFFER o
        JOIN APPLICATION a ON o.app_id = a.app_id
        JOIN STUDENT s ON a.student_id = s.student_id
        JOIN JOB j ON a.job_id = j.job_id
        JOIN COMPANY c ON j.company_id = c.company_id
        ORDER BY o.offered_salary_lpa DESC
    '''
    placed_students = conn.execute(placed_query).fetchall()
    conn.close()

    return render_template('dashboard.html', 
                           students=total_students, 
                           companies=total_companies, 
                           jobs=total_jobs, 
                           offers=total_offers,
                           placed_list=placed_students)

@app.route('/students')
def students():
    conn = get_db_connection()
    query = '''
        SELECT s.student_code, s.name, s.email, s.phone, p.program_name, 
               a.cgpa, a.active_backlogs, a.tenth_percentage, a.twelfth_percentage
        FROM STUDENT s
        LEFT JOIN PROGRAM p ON s.program_id = p.program_id
        LEFT JOIN ACADEMIC_RECORD a ON s.student_id = a.student_id
        ORDER BY s.student_id ASC
    '''
    student_records = conn.execute(query).fetchall()
    conn.close()
    return render_template('students.html', students=student_records)

@app.route('/jobs')
def jobs():
    conn = get_db_connection()
    query_jobs = '''
        SELECT j.job_id, j.job_title, c.company_name, c.location, j.package_lpa, j.drive_date,
               e.min_cgpa, e.max_backlogs_allowed
        FROM JOB j
        JOIN COMPANY c ON j.company_id = c.company_id
        JOIN JOB_ELIGIBILITY e ON j.job_id = e.job_id
    '''
    query_apps = '''
        SELECT s.name, s.student_code, c.company_name, j.job_title, a.status, a.application_date
        FROM APPLICATION a
        JOIN STUDENT s ON a.student_id = s.student_id
        JOIN JOB j ON a.job_id = j.job_id
        JOIN COMPANY c ON j.company_id = c.company_id
        ORDER BY a.app_id DESC
    '''
    all_jobs = conn.execute(query_jobs).fetchall()
    all_apps = conn.execute(query_apps).fetchall()
    all_students = conn.execute('SELECT student_id, name, student_code FROM STUDENT ORDER BY name ASC').fetchall()
    conn.close()
    return render_template('jobs.html', jobs=all_jobs, applications=all_apps, students=all_students)

@app.route('/apply', methods=['POST'])
def apply():
    student_id = request.form['student_id']
    job_id = request.form['job_id']
    
    conn = get_db_connection()
    student_record = conn.execute('SELECT cgpa, active_backlogs FROM ACADEMIC_RECORD WHERE student_id = ?', (student_id,)).fetchone()
    job_criteria = conn.execute('SELECT min_cgpa, max_backlogs_allowed FROM JOB_ELIGIBILITY WHERE job_id = ?', (job_id,)).fetchone()
    
    if not student_record:
        flash("Academic record not found for student!", "danger")
    elif student_record['cgpa'] < job_criteria['min_cgpa']:
        flash(f"Application Rejected: CGPA ({student_record['cgpa']}) is below required minimum ({job_criteria['min_cgpa']}).", "warning")
    elif student_record['active_backlogs'] > job_criteria['max_backlogs_allowed']:
        flash(f"Application Rejected: Active backlogs ({student_record['active_backlogs']}) exceed allowed limit ({job_criteria['max_backlogs_allowed']}).", "warning")
    else:
        try:
            conn.execute('INSERT INTO APPLICATION (student_id, job_id, status) VALUES (?, ?, ?)', (student_id, job_id, 'APPLIED'))
            conn.commit()
            flash("Application Submitted Successfully!", "success")
        except sqlite3.IntegrityError:
            flash("You have already applied for this job!", "info")
            
    conn.close()
    return redirect(url_for('jobs'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)