-- 1. SELECT Query
SELECT * FROM STUDENT;

-- 2. Aggregate Query
SELECT c.company_name, COUNT(j.job_id) AS total_drives 
FROM COMPANY c 
JOIN JOB j ON c.company_id = j.company_id 
GROUP BY c.company_name;

-- 3. Multi-table JOIN
SELECT s.name, s.student_code, j.job_title, c.company_name, a.status 
FROM APPLICATION a
JOIN STUDENT s ON a.student_id = s.student_id
JOIN JOB j ON a.job_id = j.job_id
JOIN COMPANY c ON j.company_id = c.company_id;

-- 4. Subquery
SELECT name, email FROM STUDENT 
WHERE student_id IN (
    SELECT student_id FROM ACADEMIC_RECORD WHERE cgpa >= 8.0
);
-- ===================================================
-- PLACEMENT MANAGEMENT SYSTEM: JOIN OPERATIONS
-- ===================================================

-- 1. JOIN STUDENT and PROGRAM (Shows student details with their department)
SELECT 
    s.student_code,
    s.name AS student_name,
    p.program_name,
    p.department
FROM STUDENT s
JOIN PROGRAM p ON s.program_id = p.program_id;


-- 2. JOIN COMPANY and JOB (Shows job roles offered by each company)
SELECT 
    c.company_name,
    c.location,
    j.job_title,
    j.package_lpa,
    j.drive_date
FROM COMPANY c
JOIN JOB j ON c.company_id = j.company_id;


-- 3. JOIN STUDENT, APPLICATION, and JOB (Shows who applied to which job)
SELECT 
    s.name AS student_name,
    j.job_title,
    a.application_date,
    a.status
FROM APPLICATION a
JOIN STUDENT s ON a.student_id = s.student_id
JOIN JOB j ON a.job_id = j.job_id;