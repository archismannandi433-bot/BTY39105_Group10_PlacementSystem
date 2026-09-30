INSERT INTO PROGRAM (program_name, department) VALUES 
('B.Tech CSE - Cyber Security', 'CSE'),
('B.Tech CSE - Data Science', 'CSE'),
('B.Tech CSE - Artificial Intelligence', 'CSE'),
('B.Tech ECE - Electronics & Comm', 'ECE'),
('BCA - Computer Applications', 'IT');

INSERT INTO STUDENT (student_code, name, email, phone, program_id) VALUES 
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
('BWU/BCC/25/022', 'Rishi Verma', 'rishi.v@example.com', '9876543231', 3);

INSERT INTO ACADEMIC_RECORD (student_id, cgpa, active_backlogs, tenth_percentage, twelfth_percentage) VALUES 
(1, 8.8, 0, 88.5, 85.0), (2, 7.8, 0, 82.0, 79.0), (3, 6.2, 1, 75.0, 70.0),
(4, 9.2, 0, 92.0, 90.0), (5, 8.1, 0, 85.0, 84.0), (6, 6.8, 2, 72.0, 68.0),
(7, 8.6, 0, 89.0, 86.5), (8, 7.4, 0, 78.0, 76.0), (9, 8.9, 0, 91.0, 88.0),
(10, 6.5, 1, 70.0, 67.0), (11, 7.9, 0, 81.0, 80.0), (12, 9.5, 0, 96.0, 94.0),
(13, 8.3, 0, 86.0, 83.0), (14, 6.1, 2, 68.0, 65.0), (15, 7.2, 0, 76.0, 74.0),
(16, 8.7, 0, 88.0, 87.0), (17, 8.4, 0, 87.0, 85.0), (18, 5.9, 1, 65.0, 62.0),
(19, 7.6, 0, 80.0, 78.0), (20, 8.0, 0, 83.0, 81.0), (21, 9.1, 0, 93.0, 91.0),
(22, 6.9, 0, 73.0, 71.0);

INSERT INTO COMPANY (company_name, industry, contact_email, location) VALUES 
('TCS', 'IT Services', 'hr@tcs.com', 'Kolkata'),
('Microsoft', 'Product Development', 'recruitment@microsoft.com', 'Bangalore'),
('Cognizant', 'IT & Consulting', 'careers@cognizant.com', 'Kolkata'),
('Amazon', 'E-Commerce / Cloud', 'university@amazon.com', 'Hyderabad'),
('Wipro', 'IT Services', 'campus@wipro.com', 'Pune'),
('Deloitte', 'Financial Consulting', 'graduates@deloitte.com', 'Gurgaon');

INSERT INTO JOB (company_id, job_title, package_lpa, drive_date) VALUES 
(1, 'System Engineer', 3.6, '2026-10-15'),
(2, 'Software Engineer', 14.0, '2026-11-01'),
(3, 'Programmer Analyst', 4.2, '2026-10-20'),
(4, 'SDE-1', 18.5, '2026-11-10'),
(5, 'Project Engineer', 3.8, '2026-10-25'),
(6, 'Risk Analyst', 7.5, '2026-11-05'),
(1, 'Digital Software Engineer', 7.0, '2026-10-18');

INSERT INTO JOB_ELIGIBILITY (job_id, min_cgpa, max_backlogs_allowed) VALUES 
(1, 6.5, 1), (2, 8.0, 0), (3, 6.0, 1), (4, 8.5, 0), (5, 6.0, 1), (6, 7.0, 0), (7, 7.5, 0);

INSERT INTO APPLICATION (student_id, job_id, status) VALUES 
(1, 1, 'OFFERED'), (2, 1, 'OFFERED'), (4, 2, 'OFFERED'), (5, 2, 'OFFERED'), (7, 2, 'OFFERED'),
(9, 4, 'OFFERED'), (12, 4, 'OFFERED'), (13, 3, 'OFFERED'), (16, 6, 'OFFERED'), (17, 7, 'OFFERED'),
(21, 4, 'OFFERED'), (1, 2, 'SHORTLISTED'), (3, 1, 'APPLIED'), (8, 3, 'SHORTLISTED'), (11, 5, 'APPLIED'),
(15, 3, 'APPLIED'), (19, 5, 'SHORTLISTED'), (20, 6, 'SHORTLISTED'), (22, 5, 'APPLIED');

INSERT INTO OFFER (app_id, offer_letter_code, offered_salary_lpa, joining_date) VALUES 
(1, 'OFF-TCS-001', 3.6, '2027-06-01'), (2, 'OFF-TCS-002', 3.6, '2027-06-01'),
(3, 'OFF-MSFT-001', 14.0, '2027-07-15'), (4, 'OFF-MSFT-002', 14.0, '2027-07-15'),
(5, 'OFF-MSFT-003', 14.0, '2027-07-15'), (6, 'OFF-AMZN-001', 18.5, '2027-08-01'),
(7, 'OFF-AMZN-002', 18.5, '2027-08-01'), (8, 'OFF-CTS-001', 4.2, '2027-06-15'),
(9, 'OFF-DEL-001', 7.5, '2027-07-01'), (10, 'OFF-TCSD-001', 7.0, '2027-06-01'),
(11, 'OFF-AMZN-003', 18.5, '2027-08-01');