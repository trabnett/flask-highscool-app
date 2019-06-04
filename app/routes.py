from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from app.students import Students
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import Student, Teacher, StudentCourse, Course, Sport, Test, StudentSport, StudentTest, SportScore
from datetime import datetime
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

engine = db.engine
Session = sessionmaker(engine)
session = Session()
teacher_check = {'status': False}

@app.route('/')
def welcome():
    print(current_user, teacher_check)
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

@app.route('/students/<string:id>', methods=['GET'])
def student(id):
    print(teacher_check, "teacher_check")
    student = Student.query.filter_by(id=id).first()
    if student == None:
        return render_template('student.html', student={'alert': 'this student is not registered'})
    days = datetime.now() - student.birthday
    years = int(days.days / 365)
    student_courses = session.query(
        Student, 
        Teacher, 
        StudentCourse,
        Course,
        Test,
        StudentTest
            ).filter(
                Student.id == student.id
            ).filter(
                Course.id == StudentCourse.course_id
            ).filter(
                Teacher.id == Course.teacher_id
            ).filter(
                student.id == StudentCourse.student_id
            ).filter(
                Test.course_id == Course.id
            ).filter(
                StudentTest.student_id == student.id
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
            'teacher': entry[1].last_name,
            'teacher_id': entry[1].id,
            'grade': entry[3].grade,
            'test_scores': add_grade
            }
    gpa = []
    for course in dic:
        dic[course]['average'] = round(sum(test[1] for test in dic[course]['test_scores']) / len(dic[course]['test_scores']),1)
        gpa.append(sum(test[1] for test in dic[course]['test_scores']) / len(dic[course]['test_scores']))
    gpa = round(sum(gpa)/ len(gpa),1)
    student_sports = session.query(
        Student,
        StudentSport,
        Sport   
            ).filter(
                Sport.id == StudentSport.sport_id
            ).filter(
                student.id == StudentSport.student_id
            ).filter(
                student.id == Student.id
            ).all()
    print(student.id, student_sports)
    return render_template('student.html', student=student, years=years, courses=dic, gpa=gpa, sports=student_sports)

@app.route('/students/<string:id>', methods=['POST'])
def update_student(id):
    old_password = request.form.get("old_password")
    new_password1 = request.form.get("new_password1")
    new_password2 = request.form.get("new_password2")
    new_hash = generate_password_hash(new_password1)
    student = session.query(Student).filter_by(id = id).first()
    if check_password_hash(student.password_hash, old_password) == True:
        student.password_hash = new_hash
        print(student.password_hash, "new hash?")
        session.commit()
    else:
        message = "Invalid Password"
        flash('Invalid Password')
    return redirect(f'/students/{id}')

    print(old_password, "<=== old_password", new_password1, new_password2, hash)
    print(student)
    return redirect(f'/students/{id}')

@app.route('/teachers')
def teachers():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

@app.route('/teachers/<string:id>', methods=['GET'])
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
    teacher_sports = session.query(Sport, Teacher
        ).filter(educator.id == Teacher.id
        ).filter(Sport.coach_id == educator.id
        ).all()
    print(teacher_sports)
    return render_template('teacher.html', educator=educator, year_started=educator.started_at_school.year, courses=teacher_courses, sports=teacher_sports)

@app.route('/teachers/<string:id>', methods=['POST'])
def update_teacher(id):
    old_password = request.form.get("old_password")
    new_password1 = request.form.get("new_password1")
    new_password2 = request.form.get("new_password2")
    print(old_password, "<=== old_password", new_password1, new_password2)
    teacher = Teacher.query.filter_by(id = id).first()
    print(teacher)
    return redirect(f'/teachers/{id}')

@app.route('/sports')
def sports():
    sports = Sport.query.all()
    return render_template('sports.html', sports=sports)

@app.route('/sports/<string:name>')
def sport(name):
    if current_user.is_authenticated:
        print(current_user, "<====== current user")
    sport = Sport.query.filter_by(sport_name=name).first()
    if sport == None:
        sport = {'sport_name': 'no such sport exists'}
        return render_template('sport.html', sport=sport)
    sport_summary = session.query(StudentSport, Student
    ).filter(sport.id == StudentSport.sport_id
    ).filter(StudentSport.student_id == Student.id
    ).all()
    return render_template('sport.html', sport=sport, summary=sport_summary)

@app.route('/students/<string:id>/sports/<string:name>/delete', methods=['POST'])
def delete(name, id):
    sport = session.query(Student, Sport, StudentSport
    ).filter(id == Student.id
    ).filter(name == Sport.sport_name
    ).filter(Sport.id == StudentSport.sport_id
    ).filter(id == StudentSport.student_id).all()
    print(sport[0][2].id, "<===jeyyyyy")
    session.delete(sport[0][2])
    session.commit()
    return redirect(f'/students/{id}')
