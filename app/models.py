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
    grade = db.Column(db.Integer)
    pic_url = db.Column(db.String(240)) 
    twitter = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Student {}>'.format(self.last_name)

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
    pic_url = db.Column(db.String(240)) 
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

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    test_name = db.Column(db.String(64))

    def __repr__(self):
        return '<Test {}>'.format(self.test_name)

class StudentTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    score = db.Column(db.Integer)

    def __repr__(self):
        return '<StudentTest {}>'.format(self.id)

class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport_name = db.Column(db.String)
    coach_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return '<Sport {}>'.format(self.sport_name)

class StudentSport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))

    def __repr__(self):
        return '<StudentSport {}>'.format(self.id)

class SportScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.Integer, db.ForeignKey('sport.id'))
    date = db.Column(db.DateTime())
    opponent = db.Column(db.String(64))
    trhs_score = db.Column(db.Integer)
    opponent_score = db.Column(db.Integer)

    def __repr__(self):
        return '<Score {} >'.format(self.sport)


