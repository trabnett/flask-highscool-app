from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.students import Students
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import Student, Teacher, StudentCourse, Course, Sport, Test, StudentSport, StudentTest, SportScore
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = db.engine
Session = sessionmaker(engine)
session = Session()
teacher_check = {'status': True}

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.birthday:
        teacher_check['status'] = False
        return redirect(f'/students/{current_user.id}')
    if current_user.is_authenticated and current_user.started_at_school:
        return redirect(f'/teachers/{current_user.id}')
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.username.data).first()
        if user == None:
            user = Teacher.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        if hasattr(user, 'birthday'):
            teacher_check['status'] = False
            return redirect(f'/students/{user.id}')
        if hasattr(user, 'started_at_school'):
            teacher_check['status'] = True
            return redirect(f'/teachers/{user.id}')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/students')
def students():
    enrolled_students = Student.query.all()
    return render_template('students.html', students=enrolled_students)

@app.route('/students/<string:id>')
def student(id):
    student = Student.query.filter_by(id=id).first()
    if student == None:
        return render_template('student.html', student={'alert': 'this student is not registered'})
    print(student)
    days = datetime.now() - student.birthday
    years = int(days.days / 365)
    student_courses = session.query(
        Student, 
        Teacher, 
        StudentCourse,
        Course
            ).filter(
                Student.id == student.id
            ).filter(
                Course.id == StudentCourse.course_id
            ).filter(
                Teacher.id == Course.teacher_id
            ).filter(
                student.id == StudentCourse.student_id
            ).all()
    student_sports = session.query(
        Student,
        StudentSport,
        Sport   
            ).filter(
                student.id == StudentSport.student_id
            ).filter(
                Sport.id == StudentSport.sport_id
            ).all()
    student_grades = StudentTest.query.filter(student.id == StudentTest.student_id).all()
    average = 0
    for test in student_grades:
        total += test.score
    print("the average of this student is: ", (average / len(student_grades)))
    print(student_grades)
    return render_template('student.html', student=student, years=years, courses=student_courses)

@app.route('/teachers')
def teachers():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

@app.route('/teachers/<string:id>')
def teacher(id):
    educator = {'alert': 'this teacher is not currently a part of the faculty'}
    faculty = Teacher.query.all()
    for person in faculty:
        if int(person.id) == int(id):
            educator = person
    teacher_courses = session.query(Teacher, Course
        ).filter(educator.id == Course.teacher_id
        ).filter(educator.id == Teacher.id
        ).all()
    print(teacher_courses, educator.id)
    return render_template('teacher.html', educator=educator, year_started=educator.started_at_school.year, courses=teacher_courses)

@app.route('/sports')
def sports():
    sports = Sport.query.all()
    return render_template('sports.html', sports=sports)

@app.route('/sports/<string:name>')
def sport(name):
    sport = Sport.query.filter_by(sport_name=name).first()
    if sport == None:
        sport = {'sport_name': 'no such sport exists'}
        return render_template('sport.html', sport=sport)
    sport_summary = session.query(StudentSport, Student
    ).filter(sport.id == StudentSport.sport_id
    ).filter(StudentSport.student_id == Student.id
    ).all()
    print(sport_summary)
    return render_template('sport.html', sport=sport, summary=sport_summary)