from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, TestScore
from app.students import Students
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import Student, Teacher, StudentCourse, Course, Sport, Test, StudentSport, StudentTest, SportScore
from datetime import datetime
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from app.helper_functions import get_average, get_test_scores, get_gpa

engine = db.engine
Session = sessionmaker(engine)
session = Session()
teacher_check = {'status': None}

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
        teacher_check['status'] = True
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
    academic_summary = get_test_scores(id)
    gpa = get_gpa(academic_summary)
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
    return render_template('student.html', student=student, years=years, courses=academic_summary, gpa=gpa, sports=student_sports)

@app.route('/students/<string:id>', methods=['POST'])
def update_student(id):
    old_password = request.form.get("old_password")
    new_password1 = request.form.get("new_password1")
    new_hash = generate_password_hash(new_password1)
    student = session.query(Student).filter_by(id = id).first()
    if check_password_hash(student.password_hash, old_password):
        student.password_hash = new_hash
        print(student.password_hash, "new hash?")
        session.commit()
    else:
        flash('You incorrectly entered your current password')
    return redirect(f'/students/{id}')

@app.route('/teachers')
def teachers():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

@app.route('/teachers/<string:id>', methods=['GET'])
def teacher(id):
    educator = Teacher.query.filter_by(id=id).first()
    if educator == None:
        return render_template('teacher.html', educator={'alert': 'this teacher is not currently a part of the faculty'})
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
    new_hash = generate_password_hash(new_password1)
    teacher = session.query(Teacher).filter_by(id = id).first()
    if check_password_hash(teacher.password_hash, old_password):
        teacher.password_hash = new_hash
        session.commit()
    else:
        flash('You incorrectly entered your current password')
    return redirect(f'/teachers/{id}')

@app.route('/sports')
def sports():
    num = []
    if hasattr(current_user, 'birthday'):
        student_sports = StudentSport.query.filter_by(student_id=current_user.id).all()
        for sport in student_sports:
            num.append(sport.sport_id)
    sports = session.query(Sport, Teacher).filter(
        Sport.coach_id == Teacher.id
    ).all()
    return render_template('sports.html', sports=sports, student_sports=num)

@app.route('/sports/<string:name>')
def sport(name):
    sport = Sport.query.filter_by(sport_name=name).first()
    print("<------------", sport)
    if sport == None:
        print("here?")
        return render_template('sport.html', alert='no such sport exists')
    sport_summary = session.query(StudentSport, Student, Teacher, Sport
    ).filter(sport.id == StudentSport.sport_id
    ).filter(StudentSport.student_id == Student.id
    ).filter(Teacher.id == Sport.coach_id
    ).filter(StudentSport.sport_id == Sport.id
    ).all()
    print(sport_summary)
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

@app.route('/students/<int:id>/sports/<string:name>/join', methods=['POST'])
def join(name, id):
    sport = Sport.query.filter_by(sport_name=name).first()
    count = StudentSport.query.filter_by(sport_id=sport.id).count()
    print(count)
    if count >= sport.max_size:
        flash('This team is full. You cannot register right now.')
        return  redirect(f'/sports/{name}')
    new_student_sport = StudentSport(sport_id = sport.id, student_id = id)
    session.add(new_student_sport)
    session.commit()
    return redirect(f'/sports/{name}')

@app.route('/courses')
def courses():
    courses = session.query(Course, Teacher
    ).filter(Teacher.id == Course.teacher_id).order_by(Course.grade).all()
    print(courses)
    return render_template('courses.html', courses=courses)

@app.route('/courses/<int:id>')
def course(id):
    course = session.query(Course, StudentCourse, Student, Teacher
    ).filter(id == Course.id
    ).filter(StudentCourse.course_id == Course.id
    ).filter(Student.id == StudentCourse.student_id
    ).filter(Course.teacher_id == Teacher.id).all()
    return render_template('course.html', course=course, get_average=get_average)

@app.route('/courses/<int:id>/new_test', methods=['GET', 'POST'])
def new_test(id):
    print(request.form, "heyyyyyy")
    if request.method == 'POST':
        test_name = request.form.get('test_name')
        new_test = Test(course_id = id, test_name = test_name)
        session.add(new_test)
        session.commit()
        form_data = request.form
        for key in form_data.keys():
            for value in form_data.getlist(key):
                if key != 'test_name':
                    new_student_test = StudentTest(test_id = new_test.id, student_id = key, score = value)
                    session.add(new_student_test)
                    session.commit()
    form = TestScore()
    if form.validate_on_submit():
        print(form.student.data, form.test.data, form.score.data, "heyy moooo")
    course_summary = session.query(Course, StudentCourse, Student, Teacher
    ).filter(id == Course.id
    ).filter(StudentCourse.course_id == Course.id
    ).filter(Student.id == StudentCourse.student_id
    ).filter(Course.teacher_id == Teacher.id).all()
    print(course_summary)
    return render_template('new_test.html', course_summary=course_summary, form=form)