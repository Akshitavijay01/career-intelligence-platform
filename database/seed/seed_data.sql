-- Seed data for Career Intelligence Platform
-- This creates sample opportunities for testing and demonstration

-- Insert skills
INSERT INTO skills (name, category) VALUES
('python', 'programming'),
('javascript', 'programming'),
('java', 'programming'),
('c++', 'programming'),
('react', 'frontend'),
('angular', 'frontend'),
('vue', 'frontend'),
('node', 'backend'),
('express', 'backend'),
('django', 'backend'),
('flask', 'backend'),
('sql', 'database'),
('postgresql', 'database'),
('mongodb', 'database'),
('mysql', 'database'),
('aws', 'cloud'),
('docker', 'devops'),
('kubernetes', 'devops'),
('git', 'tools'),
('machine learning', 'ai'),
('tensorflow', 'ai'),
('pandas', 'data science'),
('numpy', 'data science'),
('html', 'frontend'),
('css', 'frontend'),
('typescript', 'programming'),
('rest api', 'backend'),
('graphql', 'backend'),
('linux', 'operating system'),
('bash', 'scripting'),
('jenkins', 'devops'),
('terraform', 'devops');

-- Insert sample opportunities
INSERT INTO opportunities (title, company, description, location, work_type, stipend, employment_type, education_requirements, experience_requirements, application_deadline, application_url, source, posting_date, status, is_verified) VALUES
(
    'Python Developer Intern',
    'Tech Solutions India',
    'We are looking for a Python Developer Intern to join our backend team. You will work on developing scalable APIs and microservices using Python and Django. This is a great opportunity to learn industry best practices and work on real-world projects.',
    'Bangalore',
    'remote',
    25000,
    'internship',
    'BCA, B.Tech, or related degree',
    'No prior experience required',
    '2026-10-15',
    'https://techsolutions.example.com/careers/python-intern',
    'demo',
    '2026-09-01',
    'active',
    true
),
(
    'Frontend Developer Intern',
    'WebWiz Solutions',
    'Join our frontend team to build beautiful, responsive user interfaces using React and modern CSS. You will collaborate with designers and backend developers to create seamless user experiences.',
    'Mumbai',
    'hybrid',
    20000,
    'internship',
    'BCA, B.Sc Computer Science, or related',
    'Basic knowledge of HTML, CSS, JavaScript',
    '2026-10-30',
    'https://webwiz.example.com/careers/frontend-intern',
    'demo',
    '2026-09-01',
    'active',
    true
),
(
    'Data Science Intern',
    'DataVenture Analytics',
    'Exciting opportunity for aspiring data scientists! Work on real-world datasets, build machine learning models, and derive insights that drive business decisions. You will work with Python, Pandas, and scikit-learn.',
    'Hyderabad',
    'on-site',
    30000,
    'internship',
    'B.Tech, M.Tech in Computer Science, Statistics, or related',
    'Knowledge of Python and basic statistics',
    '2026-11-15',
    'https://dataventure.example.com/careers/data-science-intern',
    'demo',
    '2026-09-01',
    'active',
    true
),
(
    'Full Stack Developer Intern',
    'StartupHub',
    'Join our fast-growing startup as a Full Stack Developer Intern. You will work on both frontend (React) and backend (Node.js) technologies. Great learning opportunity with mentorship from senior engineers.',
    'Bangalore',
    'hybrid',
    35000,
    'internship',
    'BCA, B.Tech, or related technical degree',
    'Basic knowledge of JavaScript and databases',
    '2026-10-20',
    'https://startuphub.example.com/careers/fullstack-intern',
    'demo',
    '2026-09-01',
    'active',
    true
),
(
    'DevOps Engineer Intern',
    'CloudScale Technologies',
    'Learn cloud infrastructure and DevOps practices! You will work with Docker, Kubernetes, and CI/CD pipelines. Support our platform engineering team in deploying and maintaining cloud-native applications.',
    'Pune',
    'on-site',
    28000,
    'internship',
    'BCA, B.Tech in Computer Science or related',
    'Basic understanding of Linux and command line',
    '2026-11-30',
    'https://cloudscale.example.com/careers/devops-intern',
    'demo',
    '2026-09-01',
    'active',
    true
),
(
    'Machine Learning Intern',
    'AI Labs India',
    'Work on cutting-edge AI projects! You will develop machine learning models, work with neural networks, and contribute to research projects. Experience with TensorFlow or PyTorch is a plus.',
    'Bangalore',
    'remote',
    40000,
    'internship',
    'M.Tech or PhD in AI/ML, Computer Science, or related',
    'Knowledge of Python and machine learning concepts',
    '2026-12-15',
    'https://ailabs.example.com/careers/ml-intern',
    'demo',
    '2026-09-01',
    'active',
    true
),
(
    'Web Development Intern',
    'DigitalCraft Agency',
    'Creative agency looking for web developers to build websites and web applications. You will work with HTML, CSS, JavaScript, and WordPress. Great for building portfolio!',
    'Chennai',
    'hybrid',
    18000,
    'internship',
    'Any technical degree',
    'No experience required',
    '2026-10-25',
    'https://digitalcraft.example.com/careers/web-dev-intern',
    'demo',
    '2026-09-01',
    'active',
    true
),
(
    'Backend Developer Intern',
    'APIFirst Solutions',
    'Build robust APIs and microservices! You will work with Node.js, Express, and PostgreSQL. Learn about RESTful design, database optimization, and server-side architecture.',
    'Bangalore',
    'remote',
    26000,
    'internship',
    'BCA, B.Tech, or related degree',
    'Basic programming knowledge',
    '2026-11-10',
    'https://apifirst.example.com/careers/backend-intern',
    'demo',
    '2026-09-01',
    'active',
    true
),
(
    'Mobile App Developer Intern',
    'Appverse Studios',
    'Develop mobile applications for iOS and Android! Work with React Native or Flutter to build cross-platform apps. Great opportunity to learn mobile development from scratch.',
    'Delhi',
    'hybrid',
    22000,
    'internship',
    'BCA, B.Tech, or related degree',
    'Basic programming knowledge preferred',
    '2026-10-30',
    'https://appverse.example.com/careers/mobile-intern',
    'demo',
    '2026-09-01',
    'active',
    true
),
(
    'Software Engineering Intern',
    'ProductFirst Corp',
    'General software engineering role where you will work on various projects based on your interests and skills. Rotational program covering frontend, backend, and DevOps.',
    'Bangalore',
    'hybrid',
    30000,
    'internship',
    'B.Tech in Computer Science or related',
    'Strong programming fundamentals',
    '2026-11-20',
    'https://productfirst.example.com/careers/swe-intern',
    'demo',
    '2026-09-01',
    'active',
    true
);

-- Add skills to opportunities
-- Python Developer Intern (skill: python, sql, django, docker)
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 1, id, true FROM skills WHERE name = 'python';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 1, id, true FROM skills WHERE name = 'sql';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 1, id, false FROM skills WHERE name = 'django';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 1, id, false FROM skills WHERE name = 'docker';

-- Frontend Developer Intern (skill: html, css, javascript, react)
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 2, id, true FROM skills WHERE name = 'html';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 2, id, true FROM skills WHERE name = 'css';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 2, id, true FROM skills WHERE name = 'javascript';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 2, id, false FROM skills WHERE name = 'react';

-- Data Science Intern (skill: python, pandas, numpy, machine learning)
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 3, id, true FROM skills WHERE name = 'python';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 3, id, true FROM skills WHERE name = 'pandas';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 3, id, false FROM skills WHERE name = 'numpy';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 3, id, false FROM skills WHERE name = 'machine learning';

-- Full Stack Developer Intern (skill: react, node, sql, javascript)
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 4, id, true FROM skills WHERE name = 'react';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 4, id, true FROM skills WHERE name = 'node';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 4, id, true FROM skills WHERE name = 'javascript';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 4, id, false FROM skills WHERE name = 'sql';

-- DevOps Engineer Intern (skill: docker, kubernetes, aws, linux)
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 5, id, true FROM skills WHERE name = 'docker';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 5, id, true FROM skills WHERE name = 'linux';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 5, id, false FROM skills WHERE name = 'kubernetes';
INSERT INTO opportunity_skills (opportunity_id, skill_id, is_required)
SELECT 5, id, false FROM skills WHERE name = 'aws';