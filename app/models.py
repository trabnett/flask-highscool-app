from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from app import login
import app.routes

@login.user_loader
def load_user(id):
    if app.routes.teacher_check['status'] == False:
        user = Student.query.get(id)
        return user
    user = Teacher.query.get(id)
    return user



class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    birthday = db.Column(db.DateTime())
    twitter = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.last_name)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    course_name = db.Column(db.String(64))
    grade = db.Column(db.Integer)

    def __repr__(self):
        return '<Course {}>'.format(self.course_name)

class Teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    started_at_school = db.Column(db.DateTime())
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Teacher {}>'.format(self.last_name)

class StudentCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return '<StudentCourse {}>'.format(self.id)
