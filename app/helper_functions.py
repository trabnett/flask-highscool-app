from app import app, db
from app.models import Student, Teacher, StudentCourse, Course, Sport, Test, StudentSport, StudentTest, SportScore
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from flask_login import current_user

engine = db.engine
Session = sessionmaker(engine)
session = Session()

def hello(thing):
    print("hello", thing)

def get_average(student_id, name):
    res = []
    grades = session.query(StudentTest, Course, Test
    ).filter(StudentTest.student_id == student_id
    ).filter(Course.course_name == name
    ).filter(StudentTest.test_id == Test.id
    ).filter(Test.course_id == Course.id).all()
    for grade in grades:
        res.append(grade[0].score)
    return(sum(res) / len(res))