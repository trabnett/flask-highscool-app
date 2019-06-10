from app import app, db
from app.models import Student, Teacher, StudentCourse, Course, Sport, Test, StudentSport, StudentTest, SportScore
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from flask_login import current_user

engine = db.engine
Session = sessionmaker(engine)
session = Session()


def get_average(student_id, name):
    res = []
    grades = session.query(StudentTest, Course, Test
    ).filter(StudentTest.student_id == student_id
    ).filter(Course.course_name == name
    ).filter(StudentTest.test_id == Test.id
    ).filter(Test.course_id == Course.id).all()
    for grade in grades:
        res.append(grade[0].score)
    return round((sum(res) / len(res)), 1)

def get_test_scores(student_id):
    student_courses = session.query(
    Student, 
    Teacher, 
    StudentCourse,
    Course,
    Test,
    StudentTest
        ).filter(
            Student.id == student_id
        ).filter(
            Course.id == StudentCourse.course_id
        ).filter(
            Teacher.id == Course.teacher_id
        ).filter(
            student_id == StudentCourse.student_id
        ).filter(
            Test.course_id == Course.id
        ).filter(
            StudentTest.student_id == student_id
        ).filter(
            Test.id == StudentTest.test_id
        ).all()
    dic = {}
    for entry in student_courses:
        add_grade = []
        if entry[3].course_name in dic and 'test_scores' in dic[entry[3].course_name]:
            add_grade = dic[entry[3].course_name]['test_scores']
            add_grade.append([entry[4].test_name, entry[5].score])
        else:
            add_grade = [[entry[4].test_name, entry[5].score]]
        dic[entry[3].course_name] = {
            'course_id': entry[3].id,
            'teacher': entry[1].last_name,
            'teacher_id': entry[1].id,
            'grade': entry[3].grade,
            'test_scores': add_grade
            }
    for course in dic:
        dic[course]['average'] = round(sum(test[1] for test in dic[course]['test_scores']) / len(dic[course]['test_scores']),1)
    return dic

def get_gpa(academic_summary):
    gpa = []
    for course in academic_summary:
        gpa.append(sum(test[1] for test in academic_summary[course]['test_scores']) / len(academic_summary[course]['test_scores']))
    gpa = round(sum(gpa)/ len(gpa),1)
    return gpa