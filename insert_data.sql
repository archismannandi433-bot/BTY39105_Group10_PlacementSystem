-- Clean previous entries
DELETE FROM APPLICATION;
DELETE FROM JOB_ELIGIBILITY;
DELETE FROM JOB;
DELETE FROM COMPANY;
DELETE FROM ACADEMIC_RECORD;
DELETE FROM STUDENT;
DELETE FROM PROGRAM;
DELETE FROM USERS;

-- Reset Auto-Increment Counters
DELETE FROM sqlite_sequence;

-- ===================================================
-- 1. ACADEMIC PROGRAMS & ADMIN USER
-- ===================================================

INSERT INTO PROGRAM (program_id, program_name, department) VALUES 
(1, 'B.Tech CSE - Cyber Security', 'CSE'),
(2, 'B.Tech CSE - Data Science', 'CSE'),
(3, 'B.Tech ECE', 'ECE'),
(4, 'B.Tech Mechanical Engineering', 'ME');

-- Admin Account (email: admin@placement.com | pass: adminpassword)
INSERT INTO USERS (user_id, email, password_hash, role) VALUES 
(1, 'admin@placement.com', 'adminpassword', 'ADMIN');


-- ===================================================
-- 2. SEED 105 REALISTIC STUDENTS
-- ===================================================

-- Create 105 Student User Accounts (IDs 101 to 205)
WITH RECURSIVE cnt(x) AS (
    SELECT 101
    UNION ALL
    SELECT x + 1 FROM cnt WHERE x < 205
)
INSERT INTO USERS (user_id, email, password_hash, role)
SELECT 
    x,
    'student' || (x - 100) || '@placement.com',
    'studentpassword',
    'STUDENT'
FROM cnt;

-- Temp table of first and last names to synthesize realistic combinations
CREATE TEMP TABLE student_names (id INTEGER PRIMARY KEY, full_name TEXT);
INSERT INTO student_names (full_name) VALUES
('Pritam Goldar'), ('Arijit Roy'), ('Sneha Banerjee'), ('Rahul Mukherjee'), ('Ananya Chakraborty'),
('Sayan Dutta'), ('Debolina Das'), ('Rohan Sharma'), ('Priya Verma'), ('Vikram Singh'),
('Amit Kumar'), ('Neha Gupta'), ('Rishabh Mishra'), ('Anushka Bose'), ('Siddharth Ghosh'),
('Shweta Nair'), ('Arpan Chatterji'), ('Tiyasa Sen'), ('Sourav Paul'), ('Megha Saha'),
('Abhishek Bhattacharya'), ('Tanvi Saxena'), ('Karan Malhotra'), ('Pooja Kulkarni'), ('Manish Pandey'),
('Ritu Deshmukh'), ('Aditya Iyer'), ('Kriti Reddy'), ('Varun Agarwal'), ('Riya Pal'),
('Subhajit Nandi'), ('Sayani Bishnu'), ('Niladri Chaudhuri'), ('Sreeja Seal'), ('Arkadeep Ganguly'),
('Payel Kundu'), ('Suraj Mondal'), ('Trisha De'), ('Bishal Dhar'), ('Dipanwita Kole'),
('Kaustav Biswas'), ('Moumitha Majumder'), ('Sujay Haldar'), ('Shreyasi Sikdar'), ('Rana Sarkar'),
('Pallabi Nag'), ('Tuhin Som'), ('Sanchari Barat'), ('Koushik Paria'), ('Swagata Maiti'),
('Ayan Pramanik'), ('Brinda Ghosh'), ('Chiranjit Bag'), ('Damini Roy'), ('Eshan Samanta'),
('Farhan Ali'), ('Gourab Kar'), ('Himika Mitra'), ('Indranil Rakshit'), ('Jaya Chandra'),
('Kushal Sanyal'), ('Lopamudra Hazra'), ('Mayukh Dawn'), ('Nandini Barat'), ('Omkar Joshi'),
('Partha Sarathi'), ('Qasim Khan'), ('Rupali Mallick'), ('Sudipta Bhowmick'), ('Tania Sur'),
('Ujjwal Barman'), ('Vaishali Kapoor'), ('Wasim Akram'), ('Yashvardhan Jain'), ('Zoya Akhtar'),
('Aritra Bera'), ('Barnali Saha'), ('Chayan Ghosal'), ('Divya Nair'), ('Gautam Rao'),
('Harsh Vardhan'), ('Isha Sinha'), ('Jitendra Prasad'), ('Kavita Mehra'), ('Lokesh Hegde'),
('Mohit Suri'), ('Nisha Pillai'), ('Oindrila Roy'), ('Prateek Chouhan'), ('Rashmi Menon'),
('Sarbani Kar'), ('Tarun Kapoor'), ('Upasana Sen'), ('Vivek Oberoi'), ('Yamini Krishnamurthy'),
('Zaheer Khan'), ('Akash Deep'), ('Bhabatosh Giri'), ('Chandrima Poddar'), ('Debasmita Laha'),
('Gouranga Santra'), ('Hrittika Bhawal'), ('Ishan Kishan'), ('Jasprit Bumrah'), ('Kunal Khemu');

-- Populate STUDENT profiles
INSERT INTO STUDENT (student_id, user_id, student_code, name, email, phone, program_id)
SELECT 
    sn.id,
    sn.id + 100,
    'BWU/BCC/25/' || PRINTF('%03d', sn.id),
    sn.full_name,
    'student' || sn.id || '@placement.com',
    '987' || PRINTF('%07d', 6543210 + sn.id),
    ((sn.id - 1) % 4) + 1
FROM student_names sn;

DROP TABLE student_names;

-- Populate ACADEMIC_RECORDs for all 105 Students
WITH RECURSIVE cnt(x) AS (
    SELECT 1
    UNION ALL
    SELECT x + 1 FROM cnt WHERE x < 105
)
INSERT INTO ACADEMIC_RECORD (student_id, cgpa, active_backlogs, tenth_percentage, twelfth_percentage)
SELECT 
    x,
    ROUND(6.2 + (x % 37) * 0.1, 1),
    CASE WHEN x % 12 = 0 THEN 1 ELSE 0 END,
    ROUND(75.0 + (x % 20) * 0.8, 1),
    ROUND(72.0 + (x % 20) * 0.8, 1)
FROM cnt;


-- ===================================================
-- 3. SEED 52 REAL RECRUITING COMPANIES
-- ===================================================

-- Create 52 Company User Accounts (IDs 501 to 552)
WITH RECURSIVE cnt(x) AS (
    SELECT 501
    UNION ALL
    SELECT x + 1 FROM cnt WHERE x < 552
)
INSERT INTO USERS (user_id, email, password_hash, role)
SELECT 
    x,
    'recruiter' || (x - 500) || '@corporate.com',
    'companypassword',
    'COMPANY'
FROM cnt;

-- Temp table of Real Companies
CREATE TEMP TABLE company_list (id INTEGER PRIMARY KEY, name TEXT, industry TEXT, location TEXT);
INSERT INTO company_list (name, industry, location) VALUES
('Tata Consultancy Services', 'IT Services', 'Kolkata'),
('Cognizant', 'IT Services', 'Kolkata'),
('Infosys', 'IT Services', 'Bengaluru'),
('Wipro', 'IT Services', 'Bengaluru'),
('Microsoft', 'Software Product', 'Bengaluru'),
('Google', 'Software Product', 'Hyderabad'),
('Amazon', 'E-Commerce / Cloud', 'Hyderabad'),
('Accenture', 'Consulting / IT', 'Kolkata'),
('Capgemini', 'IT Services', 'Pune'),
('IBM', 'IT & Cloud Services', 'Bengaluru'),
('HCLTech', 'IT Services', 'Noida'),
('Tech Mahindra', 'IT Services', 'Pune'),
('Oracle', 'Database & Cloud', 'Bengaluru'),
('Deloitte', 'Financial Consulting', 'Hyderabad'),
('PwC', 'Consulting Services', 'Kolkata'),
('EY (Ernst & Young)', 'Consulting Services', 'Kolkata'),
('KPMG', 'Consulting Services', 'Gurugram'),
('LTIMindtree', 'IT Services', 'Mumbai'),
('Cisco', 'Networking & Tech', 'Bengaluru'),
('Intel', 'Semiconductor', 'Bengaluru'),
('Qualcomm', 'Semiconductor', 'Hyderabad'),
('Samsung R&D', 'Electronics & Tech', 'Bengaluru'),
('Adobe', 'Software Product', 'Noida'),
('Salesforce', 'Cloud CRM', 'Hyderabad'),
('SAP', 'Enterprise Software', 'Bengaluru'),
('Goldman Sachs', 'Investment Banking', 'Bengaluru'),
('JPMorgan Chase', 'Financial Services', 'Hyderabad'),
('Morgan Stanley', 'Financial Services', 'Mumbai'),
('PayPal', 'Fintech', 'Chennai'),
('Flipkart', 'E-Commerce', 'Bengaluru'),
('Uber', 'Mobility & Tech', 'Hyderabad'),
('Swiggy', 'Consumer Tech', 'Bengaluru'),
('Zomato', 'Consumer Tech', 'Gurugram'),
('Paytm', 'Fintech', 'Noida'),
('PhonePe', 'Fintech', 'Bengaluru'),
('Amdocs', 'Telecom Software', 'Pune'),
('Nvidia', 'AI Hardware', 'Bengaluru'),
('Synopsis', 'Semiconductor Tech', 'Noida'),
('Cadence Design Systems', 'Semiconductor Tech', 'Noida'),
('Dell Technologies', 'Hardware & IT', 'Bengaluru'),
('HP Enterprise', 'Enterprise IT', 'Bengaluru'),
('L&T Technology Services', 'Engineering Services', 'Mumbai'),
('Siemens', 'Industrial Tech', 'Mumbai'),
('Bosch', 'Automotive & Tech', 'Bengaluru'),
('General Electric (GE)', 'Industrial Conglomerate', 'Bengaluru'),
('Schneider Electric', 'Energy & Automation', 'Gurugram'),
('Reliance Jio', 'Telecom & Digital', 'Mumbai'),
('Airtel', 'Telecom', 'Gurugram'),
('Thoughtworks', 'Software Consulting', 'Bengaluru'),
('Persistent Systems', 'Software Product Eng', 'Pune'),
('Cyient', 'Engineering Solutions', 'Hyderabad'),
('KPIT Technologies', 'Automotive Software', 'Pune');

-- Populate COMPANY profiles
INSERT INTO COMPANY (company_id, user_id, company_name, industry, contact_email, location)
SELECT 
    cl.id,
    cl.id + 500,
    cl.name,
    cl.industry,
    'recruiter' || cl.id || '@corporate.com',
    cl.location
FROM company_list cl;

DROP TABLE company_list;


-- ===================================================
-- 4. SEED PLACEMENT DRIVES & APPLICATIONS
-- ===================================================

INSERT INTO JOB (job_id, company_id, job_title, job_description, package_lpa, drive_date) VALUES 
(1, 1, 'System Engineer (Ninja / Digital)', 'Full-time software development and maintenance role.', 4.5, '2026-10-15'),
(2, 2, 'Programmer Analyst', 'Entry-level full stack application developer role.', 4.2, '2026-10-18'),
(3, 3, 'Specialist Programmer', 'Core Java, Python, and Microservices developer.', 9.5, '2026-10-22'),
(4, 4, 'Project Engineer', 'Cloud infrastructure and systems management role.', 3.6, '2026-10-25'),
(5, 5, 'Software Development Engineer (SDE-1)', 'Core software engineering role on cloud services.', 18.0, '2026-11-01'),
(6, 6, 'Associate Software Engineer', 'Scalable distributed backend services engineering.', 22.0, '2026-11-05'),
(7, 7, 'SDE - Cloud & Systems', 'AWS infrastructure engineering and development.', 16.5, '2026-11-10'),
(8, 8, 'Advanced App Engineering Analyst', 'Enterprise application modernization role.', 5.4, '2026-11-12'),
(9, 9, 'Senior Software Analyst', 'Java Spring Boot and Angular application dev.', 4.8, '2026-11-15'),
(10, 10, 'Associate Technical Consultant', 'Cloud solution architecture and AI integrations.', 7.2, '2026-11-20');

-- Eligibility Criteria
INSERT INTO JOB_ELIGIBILITY (eligibility_id, job_id, min_cgpa, max_backlogs_allowed) VALUES 
(1, 1, 6.0, 1), 
(2, 2, 6.0, 0), 
(3, 3, 7.5, 0), 
(4, 4, 6.0, 1), 
(5, 5, 8.0, 0),
(6, 6, 8.5, 0), 
(7, 7, 8.0, 0), 
(8, 8, 6.5, 0), 
(9, 9, 6.0, 0), 
(10, 10, 7.0, 0);
