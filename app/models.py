from app import db
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
import app.routes
from app import login

@login.user_loader
def load_user(id):
    user = Student.query.get(id)
    if user == None:
        user = Teacher.query.get(id)
        return user
    return user

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    birthday = db.Column(db.DateTime())
    grade = db.Column(db.Integer)
    pic_url = db.Column(db.String(240)) 
    twitter = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reset_code = db.Column(db.String(64))
    student_course = relationship('StudentCourse', cascade='delete')
    student_sport = relationship('StudentSport', cascade='delete')
    
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
    teacher = relationship('Teacher')
    test = relationship('Test', cascade='delete')
    student_course = relationship('StudentCourse', cascade='delete')

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
    reset_code = db.Column(db.String(64))
    course = relationship('Course', cascade='delete')
    sport = relationship('Sport', cascade='delete')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Teacher {}>'.format(self.last_name)

class StudentCourse(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('student_course.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = relationship('Student')
    course = relationship('Course')
    student_test = relationship('StudentTest', cascade='delete')

    def __repr__(self):
        return '<StudentCourse {}>'.format(self.id)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    test_name = db.Column(db.String(64))
    course = relationship('Course')
    student_test = relationship('StudentTest', cascade='delete')

    def __repr__(self):
        return '<Test {}>'.format(self.test_name)

class StudentTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    student_course_id = db.Column(db.Integer, db.ForeignKey('student_course.id'))
    score = db.Column(db.Integer)
    student_course = relationship('StudentCourse')
    test = relationship('Test')

    def __repr__(self):
        return '<StudentTest {}>'.format(self.id)

class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport_name = db.Column(db.String)
    coach_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    max_size = db.Column(db.Integer)
    teacher = relationship('Teacher')
    student_sport = relationship('StudentSport', cascade='delete')
    sport_score = relationship('SportScore', cascade='delete')

    def __repr__(self):
        return '<Sport {}>'.format(self.sport_name)

class StudentSport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    student = relationship('Student')
    sport = relationship('Sport')

    def __repr__(self):
        return '<StudentSport {}>'.format(self.id)

class SportScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    date = db.Column(db.DateTime())
    opponent = db.Column(db.String(64))
    trhs_score = db.Column(db.Integer)
    opponent_score = db.Column(db.Integer)
    sport = relationship('Sport')

    def __repr__(self):
        return '<Score {} >'.format(self.sport)


