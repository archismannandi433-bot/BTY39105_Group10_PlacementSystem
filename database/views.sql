CREATE VIEW vw_placed_students AS
SELECT s.student_code, s.name, c.company_name, j.job_title, o.offered_salary_lpa
FROM OFFER o
JOIN APPLICATION a ON o.app_id = a.app_id
JOIN STUDENT s ON a.student_id = s.student_id
JOIN JOB j ON a.job_id = j.job_id
JOIN COMPANY c ON j.company_id = c.company_id;