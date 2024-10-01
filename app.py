import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Collect environment variables from .env file
db_user = os.getenv('DATABASE_USER', 'ojbademosi')
db_password = os.getenv('DATABASE_PASSWORD', 'password')
db_host = os.getenv('DATABASE_HOST', 'localhost')
db_port = os.getenv('DATABASE_PORT', '5432')
db_name = os.getenv('DATABASE_NAME', 'ojbademosi')

# Construct the PostgreSQL URI with user, password, host, port, and database name
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Set debug mode based on environment variable
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']

db = SQLAlchemy(app)

# Ensure the database tables are created
with app.app_context():
    db.create_all()

# Student model
class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

# Professor model
class Professor(db.Model):
    __tablename__ = 'professors'
    professor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

# Course model with relationship to Professor
class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.professor_id'))
    professor = db.relationship('Professor', backref='courses', lazy=True)

# Enrollment model
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),)

# Grade model
class Grade(db.Model):
    __tablename__ = 'grades'
    grade_id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.enrollment_id'), nullable=False)
    grade = db.Column(db.Numeric(5, 2), nullable=False)

########################################################
#This endpoint will return all courses along with the  #
#professor assigned to each course (A)                 #
########################################################

@app.route('/api/courses', methods=['GET'])
def list_courses():
    print("Courses API was called")  # Debugging print
    courses = Course.query.join(Professor).all()
    if not courses:
        return jsonify({"message": "No courses found"}), 404
    course_list = [{'course_id': course.course_id, 'course_name': course.course_name, 'professor': course.professor.name} for course in courses]
    print(f"Courses found: {course_list}")  # Debugging print
    return jsonify(course_list), 200

# This endpoint allows students to enroll in a specific course (B)
@app.route('/api/enroll', methods=['POST'])
def enroll_student():
    print("Enroll API was called")  # Debugging print
    data = request.json
    print(f"Request data: {data}")  # Debugging print
    
    student_id = data['student_id']
    course_id = data['course_id']

    # Check if the student is already enrolled in the course
    existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if existing_enrollment:
        print("Student is already enrolled in this course")  # Debugging print
        return jsonify({"error": "Student is already enrolled in this course"}), 400
    
    # Enroll the student
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    
    try:
        db.session.commit()
        print(f"Student {student_id} enrolled in course {course_id}")  # Debugging print
        return jsonify({"message": "Student enrolled successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error enrolling student: {e}")
        return jsonify({"error": "An error occurred while enrolling the student"}), 500

# This endpoint allows professors to assign grades to students in their course. (C)
@app.route('/api/assign-grade', methods=['POST'])
def assign_grade():
    print("Assign Grade API was called")  # Debugging print
    data = request.json
    print(f"Request data: {data}")  # Debugging print
    
    enrollment_id = data['enrollment_id']
    grade = data['grade']

    # Check if the enrollment exists
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        print(f"Enrollment {enrollment_id} not found")  # Debugging print
        return jsonify({"error": "Enrollment not found"}), 404

    # Assign the grade
    new_grade = Grade(enrollment_id=enrollment_id, grade=grade)
    db.session.add(new_grade)
    db.session.commit()

    print(f"Grade {grade} assigned to enrollment {enrollment_id}")  # Debugging print
    return jsonify({"message": "Grade assigned successfully"}), 201

# This endpoint will generate a report showing the average grade for each course. (D)
@app.route('/api/average-grade', methods=['GET'])
def get_average_grade():
    print("Average Grade API was called")  # Debugging print
    
    # Perform a query to calculate the average grade per course
    avg_grades = db.session.query(Course.course_name, func.avg(Grade.grade).label('average_grade'))\
        .join(Enrollment, Enrollment.course_id == Course.course_id)\
        .join(Grade, Grade.enrollment_id == Enrollment.enrollment_id)\
        .group_by(Course.course_name).all()

    avg_grade_report = [{'course_name': row.course_name, 'average_grade': str(row.average_grade)} for row in avg_grades]
    print(f"Average grades: {avg_grade_report}")  # Debugging print
    return jsonify(avg_grade_report), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
