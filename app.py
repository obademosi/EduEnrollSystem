#Connect to loact host on system

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ojbademosi:password@localhost:5432/ojbademosi'
db = SQLAlchemy(app)

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

# Course model
class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.professor_id'))

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

@app.route('/courses', methods=['GET'])
def list_courses():
    courses = Course.query.join(Professor).all()
    course_list = [{'course_id': course.course_id, 'course_name': course.course_name, 'professor': course.professor.name} for course in courses]
    return jsonify(course_list), 200

#This endpoint allows the students to enroll in a specific course (B)
@app.route('/enroll', methods=['POST'])
def enroll_student():
    data = request.json
    student_id = data['student_id']
    course_id = data['course_id']

    # Check if the student is already enrolled in the course
    existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if existing_enrollment:
        return jsonify({"error": "Student is already enrolled in this course"}), 400
    
    # Enroll the student
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({"message": "Student enrolled successfully"}), 201

#This endpoint allows the professors to assign grades to 
#students in their course. (C)
@app.route('/assign-grade', methods=['POST'])
def assign_grade():
    data = request.json
    enrollment_id = data['enrollment_id']
    grade = data['grade']

    # Check if the enrollment exists
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404

    # Assign the grade
    new_grade = Grade(enrollment_id=enrollment_id, grade=grade)
    db.session.add(new_grade)
    db.session.commit()

    return jsonify({"message": "Grade assigned successfully"}), 201

#This endpoint will generate a report showing the Average
#grade for each course. (D)
@app.route('/average-grade', methods=['GET'])
def get_average_grade():
    # Perform a query to calculate the average grade per course
    avg_grades = db.session.query(Course.course_name, db.func.avg(Grade.grade).label('average_grade'))\
        .join(Enrollment, Enrollment.course_id == Course.course_id)\
        .join(Grade, Grade.enrollment_id == Enrollment.enrollment_id)\
        .group_by(Course.course_name).all()

    avg_grade_report = [{'course_name': row.course_name, 'average_grade': str(row.average_grade)} for row in avg_grades]
    return jsonify(avg_grade_report), 200



