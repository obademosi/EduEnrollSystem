-- Table for storing students
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Table for storing professors
CREATE TABLE professors (
    professor_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Table for storing courses
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    professor_id INT REFERENCES professors(professor_id)
);

-- Table for managing enrollments 
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    UNIQUE(student_id, course_id) -- Ensures a student can't enroll in the same course twice
);

-- Table for storing grades
CREATE TABLE grades (
    grade_id SERIAL PRIMARY KEY,
    enrollment_id INT REFERENCES enrollments(enrollment_id),
    grade DECIMAL(5,2) CHECK(grade >= 0 AND grade <= 100) -- Grades are from 0 to 100
);

-- Insert students
INSERT INTO students (name, email)
VALUES 
    ('John Doe', 'johndoe@example.com'),
    ('Jane Smith', 'janesmith@example.com'),
    ('Emily Davis', 'emilydavis@example.com'),
    ('Chris Johnson', 'chrisjohnson@example.com'),
    ('Anna Lee', 'annalee@example.com'),
    ('David Miller', 'davidmiller@example.com'),
    ('Sophia White', 'sophiawhite@example.com'),
    ('James Brown', 'jamesbrown@example.com'),
    ('Lily Clark', 'lilyclark@example.com'),
    ('Michael Green', 'michaelgreen@example.com');

-- Insert professors
INSERT INTO professors (name, email)
VALUES 
    ('Dr. Michael Brown', 'mbrown@university.edu'),
    ('Dr. Sarah Wilson', 'swilson@university.edu'),
    ('Dr. Robert King', 'rking@university.edu'),
    ('Dr. Lisa Adams', 'ladams@university.edu');

-- Insert courses
INSERT INTO courses (course_name, professor_id)
VALUES 
    ('Introduction to Computer Science', 1),
    ('Data Structures', 1),
    ('Philosophy 101', 2),
    ('Biology 101', 3),
    ('Introduction to Psychology', 4),
    ('Advanced Mathematics', 1),
    ('Physics I', 3),
    ('Ethics in Technology', 2),
    ('Machine Learning', 1),
    ('Chemistry 101', 3);

-- Insert enrollments
INSERT INTO enrollments (student_id, course_id)
VALUES 
    (1, 1), -- John Doe enrolls in Intro to CS
    (2, 1), -- Jane Smith enrolls in Intro to CS
    (3, 3), -- Emily Davis enrolls in Philosophy 101
    (4, 4), -- Chris Johnson enrolls in Biology 101
    (5, 5), -- Anna Lee enrolls in Intro to Psychology
    (6, 2), -- David Miller enrolls in Data Structures
    (7, 6), -- Sophia White enrolls in Advanced Mathematics
    (8, 7), -- James Brown enrolls in Physics I
    (9, 8), -- Lily Clark enrolls in Ethics in Technology
    (10, 9); -- Michael Green enrolls in Machine Learning

-- Insert grades
INSERT INTO grades (enrollment_id, grade)
VALUES 
    (1, 85.5), -- John Doe's grade in Intro to CS
    (2, 88.0), -- Jane Smith's grade in Intro to CS
    (3, 77.5), -- Emily Davis's grade in Philosophy 101
    (4, 91.0), -- Chris Johnson's grade in Biology 101
    (5, 82.0), -- Anna Lee's grade in Intro to Psychology
    (6, 95.0), -- David Miller's grade in Data Structures
    (7, 89.5), -- Sophia White's grade in Advanced Mathematics
    (8, 80.0), -- James Brown's grade in Physics I
    (9, 87.0), -- Lily Clark's grade in Ethics in Technology
    (10, 93.5); -- Michael Green's grade in Machine Learning

