# EduEnrollSystem
 develop a system that manages student enrollments, course scheduling, and grade tracking for a university.  The system should allow the following: Students can view available courses. Students can enroll in courses. Professors can assign grades to students. An administrator can run a report that provides the average grade per course.



Dependencies:

pip install Flask SQLAlchemy psycopg

Testing and Running the Application below:

Run the Flask app using the following:

export FLASK_APP=EduEnroll.py
flask run

Connection to Postgre APP on Mac OS
Host	localhost
Port	5432
User	your system user name 
Database	same as user
Password	********
Connection URL	postgresql://localhost

- Database Interaction: Using SQLAlchemy to interact with the PostgreSQL database. Relationships like foreign keys (ForeignKey) and constraints (e.g., unique constraints on enrollments) are directly modeled.
- API Development: Four endpoints were created to allow students to view courses, enroll in courses, professors to assign grades, and administrators to generate grade reports.



