# EduEnrollSystem
 develop a system that manages student enrollments, course scheduling, and grade tracking for a university.  The system should allow the following: Students can view available courses. Students can enroll in courses. Professors can assign grades to students. An administrator can run a report that provides the average grade per course.



Dependencies:

pip install Flask SQLAlchemy psycopg

Testing and Running the Application below:

Run the Flask app using the following:

export FLASK_APP=app.py
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

Populating schema
example:
from app import db, Student
student_john = Student(firstname='john', lastname='doe',
                       email='jd@example.com', age=23,
                       bio='Biology student')

Test and Debug:
Utilize Postman or cURL to test API endpoints.
Run Flask app and test the endpoints.

Steps:
Run the following command in your terminal from your project directory:

flask run

This will start the Flask server on your local machine (by default on http://127.0.0.1:5000/).
(Be sure to specify the route on the webpage of you will see a Not found pop up, example: http://127.0.0.1:5000/api/courses)

!You will know you're connected on local device when you see this below!
venv) (base) ojbademosi@OJs-MacBook-Pro EduEnrollSystem % flask run
 * Serving Flask app 'app.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000

Now that your Flask application is running and the database tables are created, time to test!

Use curl or your browser to test the endpoints:

* List courses: 
curl -X GET http://127.0.0.1:5000/api/courses

[{"course_id":1,"course_name":"Introduction to Computer Science","professor":"Dr. Michael Brown"},{"course_id":2,"course_name":"Data Structures","professor":"Dr. Michael Brown"},{"course_id":3,"course_name":"Philosophy 101","professor":"Dr. Sarah Wilson"},{"course_id":4,"course_name":"Biology 101","professor":"Dr. Robert King"},{"course_id":5,"course_name":"Introduction to Psychology","professor":"Dr. Lisa Adams"},{"course_id":6,"course_name":"Advanced Mathematics","professor":"Dr. Michael Brown"},{"course_id":7,"course_name":"Physics I","professor":"Dr. Robert King"},{"course_id":8,"course_name":"Ethics in Technology","professor":"Dr. Sarah Wilson"},{"course_id":9,"course_name":"Machine Learning","professor":"Dr. Michael Brown"},{"course_id":10,"course_name":"Chemistry 101","professor":"Dr. Robert King"}]


* Enroll a student: 
curl -X POST -H "Content-Type: application/json" -d '{"student_id": 1, "course_id": 2}' http://127.0.0.1:5000/api/enroll

result:
(venv) (base) ojbademosi@OJs-MacBook-Pro EduEnrollSystem % curl -X POST -H "Content-Type: application/json" -d '{"student_id": 1, "course_id": 2}' http://127.0.0.1:5000/api/enroll

{"message":"Student enrolled successfully"}

* Assign a grade: 
curl -X POST -H "Content-Type: application/json" -d '{"enrollment_id": 1, "grade": 95}' http://127.0.0.1:5000/api/assign-grade

result:
(venv) (base) ojbademosi@OJs-MacBook-Pro EduEnrollSystem % curl -X POST -H "Content-Type: application/json" -d '{"enrollment_id": 1, "grade": 95}' http://127.0.0.1:5000/api/assign-grade

{"message":"Grade assigned successfully"}

* Get average grades: 
curl -X GET http://127.0.0.1:5000/api/average-grade

result:
(venv) (base) ojbademosi@OJs-MacBook-Pro EduEnrollSystem % curl -X GET http://127.0.0.1:5000/api/average-grade

[{"average_grade":"77.5000000000000000","course_name":"Philosophy 101"},{"average_grade":"80.0000000000000000","course_name":"Physics I"},{"average_grade":"91.0000000000000000","course_name":"Biology 101"},{"average_grade":"89.5000000000000000","course_name":"Introduction to Computer Science"},{"average_grade":"89.5000000000000000","course_name":"Advanced Mathematics"},{"average_grade":"95.0000000000000000","course_name":"Data Structures"},{"average_grade":"87.0000000000000000","course_name":"Ethics in Technology"},{"average_grade":"93.5000000000000000","course_name":"Machine Learning"},{"average_grade":"82.0000000000000000","course_name":"Introduction to Psychology"}]
