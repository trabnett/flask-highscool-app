from app import app
import os
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, TestScore, NewSport, NewCourse, Register, JoinFaculty, ResetPassword, ForgotPassword
from app import db, mail
from flask_mail import Message
from flask_login import current_user, login_user, logout_user
from app.models import Student, Teacher, StudentCourse, Course, Sport, Test, StudentSport, StudentTest, SportScore
from datetime import datetime
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from app.helper_functions import get_average, get_test_scores, get_gpa
from app.mail_templates import template1
import secrets

engine = db.engine
Session = sessionmaker(engine)
session = Session()
teacher_check = {'status': None}

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
        user = Student.query.filter_by(email=form.email.data).first()
        if user == None:
            user = Teacher.query.filter_by(email=form.email.data).first()
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
    return render_template('password_templates/login.html', title='Sign In', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/students')
def students():
    enrolled_students = Student.query.all()
    return render_template('student_templates/students.html', students=enrolled_students)

@app.route('/students/<string:id>', methods=['GET'])
def student(id):
    student = Student.query.filter_by(id=id).first()
    if student == None:
        flash('There is no student with that id registered.')
        return render_template('alerts/not_found.html')
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
    return render_template('student_templates/student.html', student=student, years=years, courses=academic_summary, gpa=gpa, sports=student_sports)

@app.route('/students/<string:id>', methods=['POST'])
def update_student(id):
    old_password = request.form.get("old_password")
    new_password1 = request.form.get("new_password1")
    new_hash = generate_password_hash(new_password1)
    student = session.query(Student).filter_by(id = id).first()
    if check_password_hash(student.password_hash, old_password):
        student.password_hash = new_hash
        session.commit()
    else:
        flash('You incorrectly entered your current password')
    return redirect(f'/students/{id}')

@app.route('/students/<int:id>/delete', methods=['POST'])
def delete_student(id):
    student = Student.query.get(id)
    local_object = session.merge(student)
    session.delete(local_object)
    session.commit()
    return redirect('/register')

@app.route('/teachers')
def teachers():
    teachers = Teacher.query.all()
    return render_template('teacher_templates/teachers.html', teachers=teachers)

@app.route('/teachers/<string:id>', methods=['GET'])
def teacher(id):
    educator = Teacher.query.filter_by(id=id).first()
    if educator == None:
        flash('There is no teacher at this school with that id.')
        return render_template('alerts/not_found.html')
    teacher_courses = session.query(Teacher, Course
        ).filter(educator.id == Course.teacher_id
        ).filter(educator.id == Teacher.id
        ).all()
    teacher_sports = session.query(Sport, Teacher
        ).filter(educator.id == Teacher.id
        ).filter(Sport.coach_id == educator.id
        ).all()
    return render_template('teacher_templates/teacher.html', educator=educator, year_started=educator.started_at_school.year, courses=teacher_courses, sports=teacher_sports)

@app.route('/teachers/<string:id>', methods=['POST'])
def update_teacher(id):
    old_password = request.form.get("old_password")
    new_password1 = request.form.get("new_password1")
    new_hash = generate_password_hash(new_password1)
    teacher = session.query(Teacher).filter_by(id = id).first()
    if check_password_hash(teacher.password_hash, old_password):
        teacher.password_hash = new_hash
        session.commit()
    else:
        flash('You incorrectly entered your current password')
    return redirect(f'/teachers/{id}')

@app.route('/teachers/<int:id>/delete', methods=['POST'])
def delete_teacher(id):
    teacher = Teacher.query.get(id)
    local_object = session.merge(teacher)
    session.delete(local_object)
    session.commit()
    return redirect('/join_faculty')

@app.route('/sports', methods=['GET', 'POST'])
def sports():
    if request.method == 'POST':
        new_sport = request.form.get('sport_name')
        max_size = request.form.get('max_size')
        sport = Sport(sport_name=new_sport,coach_id=current_user.id,max_size=max_size)
        session.add(sport)
        session.commit()
        return redirect('/sports')
    num = []
    if hasattr(current_user, 'birthday'):
        student_sports = StudentSport.query.filter_by(student_id=current_user.id).all()
        for sport in student_sports:
            num.append(sport.sport_id)
    sports = session.query(Sport, Teacher).filter(
        Sport.coach_id == Teacher.id
    ).all()
    return render_template('teacher_templates/sports.html', sports=sports, student_sports=num)

@app.route('/sports/<string:name>', methods=['GET', 'POST'])
def sport(name):
    sport = Sport.query.filter_by(sport_name = name).first()
    if request.method == 'POST':
        local_object = session.merge(sport)
        session.delete(local_object)
        session.commit()
        return redirect('/')
    if sport == None:
        flash('No such sport exists!')
        return render_template('alerts/not_found.html')
    sport_summary = session.query(StudentSport, Student, Teacher, Sport
    ).filter(sport.id == StudentSport.sport_id
    ).filter(StudentSport.student_id == Student.id
    ).filter(Teacher.id == Sport.coach_id
    ).filter(StudentSport.sport_id == Sport.id
    ).all()
    return render_template('teacher_templates/sport.html', sport=sport, summary=sport_summary)

@app.route('/students/<string:id>/sports/<string:name>/delete', methods=['POST'])
def delete(name, id):
    sport = session.query(Student, Sport, StudentSport
    ).filter(id == Student.id
    ).filter(name == Sport.sport_name
    ).filter(Sport.id == StudentSport.sport_id
    ).filter(id == StudentSport.student_id).all()
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

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    form = NewCourse()
    if request.method == 'POST' and form.validate():
        check = Course.query.filter_by(course_name=request.form.get('course_name'), grade=request.form.get('grade')).first()
        if check != None:
            flash('this course already exists!')
            return redirect ('/courses/new')
        students = Student.query.filter_by(grade=form.grade.data).all()
        return render_template('teacher_templates/new_course_with_students.html', form=form, course_name=form.course_name.data, grade=form.grade.data, students=students)
    elif request.method == 'POST':
        return render_template('teacher_templates/new_course.html', form=form)
    courses = session.query(Course, Teacher
    ).filter(Teacher.id == Course.teacher_id).order_by(Course.grade).all()
    print(courses)
    return render_template('courses.html', courses=courses)

@app.route('/courses/new', methods=['GET', 'POST'])
def new_course():
    form = NewCourse()
    if request.method == 'POST' and form.validate():
        check = Course.query.filter_by(course_name=request.form.get('course_name'), grade=request.form.get('grade')).first()
        if check == None:
            y = Course(course_name=request.form.get('course_name'), grade=request.form.get('grade'), teacher_id=current_user.id)
            session.add(y)
            session.commit()
            data = request.form
            course_id = y.id
            for student in data:
                if student[:7] == 'student':
                    # same problem as '/courses/<id>/add_students where id in not autoincramemting
                    count = StudentCourse.query.order_by(StudentCourse.id.desc()).all()
                    if len(count) == 0:
                        sc_id = 1
                    else:
                        sc_id = count[0].id + 1
                    x = StudentCourse(id=sc_id, student_id = request.form.get(student), course_id=y.id)
                    session.add(x)
                    session.commit()
            return redirect(f'/courses/{course_id}')
        else:
            flash('A course with that name is already being taught in that grade')
            return redirect('/courses/new')
    return render_template('teacher_templates/new_course.html', form=form)

@app.route('/courses/<int:id>')
def course(id):
    c = Course.query.get(id)
    if c == None:
        flash('This course does not exist')
        return render_template('alerts/not_found.html')
    course = session.query(Course, StudentCourse, Student, Teacher
    ).filter(id == Course.id
    ).filter(StudentCourse.course_id == Course.id
    ).filter(Student.id == StudentCourse.student_id
    ).filter(Course.teacher_id == Teacher.id).all()
    if len(course) == 0 and c.teacher_id != current_user.id:
        return render_template('course.html', alert='This course does not exist, or there are no students registered in this course')
    return render_template('course.html', c=c, course=course, get_average=get_average)

@app.route('/courses/<int:id>/delete', methods=['POST'])
def delete_course(id):
    course = Course.query.get(id)
    db.session.delete(course)
    db.session.commit()
    return redirect(f'/teachers/{current_user.id}')

@app.route('/courses/<int:id>/remove_students', methods=['GET','POST'])
def remove_students(id):
    course = Course.query.filter_by(id=id).first()
    print(course.course_name)
    if request.method == 'POST':
        data = request.form
        for student in data:
            student_course = session.query(StudentCourse).filter_by(student_id=request.form.get(student), course_id=id).first()
            local_object = db.session.merge(student_course)
            db.session.delete(local_object)
            db.session.commit()
        return redirect(f'/courses/{id}')
    students = session.query(Student, StudentCourse
    ).filter(Student.id == StudentCourse.student_id
    ).filter(StudentCourse.course_id == id).all()
    return render_template('teacher_templates/course_remove_students.html', course=course, students=students)

@app.route('/courses/<int:id>/add_students', methods=['GET','POST'])
def add_students(id):
    course = Course.query.filter_by(id=id).first()
    if request.method == 'POST':
        data = request.form
        for student in data:
            if student[:7] == 'student':
                # !!!look into fixing this!!! Since I changed the StudentCourse.id to be a forign key, it is not autoincramenting, as a result I have to get the highest id and add 1 when adding a new StudentCourse
                count = StudentCourse.query.order_by(StudentCourse.id.desc()).all()
                if len(count) == 0:
                    sc_id = 1
                else:
                    sc_id = count[0].id + 1
                x = StudentCourse(id=sc_id, student_id = request.form.get(student), course_id=id)
                db.session.add(x)
                db.session.commit()
        return redirect(f'/courses/{id}')
    grade = course.grade
    sub = session.query(StudentCourse.student_id).filter_by(course_id=id)
    students = session.query(Student).filter(Student.grade == grade).filter(~Student.id.in_(sub)).all()
    return render_template('teacher_templates/course_add_students.html', students=students, course=course)

@app.route('/courses/<int:id>/new_test', methods=['GET', 'POST'])
def new_test(id):
    if request.method == 'POST':
        test_name = request.form.get('test_name')
        new_test = Test(course_id = id, test_name = test_name)
        session.add(new_test)
        session.commit()
        form_data = request.form
        for key in form_data.keys():
            for value in form_data.getlist(key):
                if key != 'test_name':
                    student_course = StudentCourse.query.filter_by(student_id=key, course_id=id).first()
                    new_student_test = StudentTest(test_id = new_test.id, student_course_id = student_course.id, score = value)
                    session.add(new_student_test)
                    session.commit()
        return redirect(f'/courses/{id}')
    form = TestScore()
    course_summary = session.query(Course, StudentCourse, Student, Teacher
    ).filter(id == Course.id
    ).filter(StudentCourse.course_id == Course.id
    ).filter(Student.id == StudentCourse.student_id
    ).filter(Course.teacher_id == Teacher.id).all()
    if len(course_summary) == 0:
        flash('You cannot add a test when there are no students registered in a course.')
        return redirect(f'/courses/{id}')
    return render_template('teacher_templates/new_test.html', course_summary=course_summary, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        data = request.form
        email_check = Student.query.filter_by(email=form.email.data).first()
        if email_check != None:
            flash('This email is already assigned to a student. Are you sure you are not already a student at this school?')
            return render_template('student_templates/register.html', form=form)
        new_student = Student(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, birthday=form.birthday.data, grade=int(form.grade.data), pic_url=form.pic_url.data, password_hash=generate_password_hash(form.password.data))
        if len(form.twitter.data) > 0:
            new_student.twitter = form.twitter.data
        db.session.add(new_student)
        db.session.commit()
        flash(f'Thank you {new_student.first_name}  {new_student.last_name}. You are now a registered student! Please Log in!')
        return redirect('/login')
    return render_template('student_templates/register.html', form=form)

@app.route('/join_faculty', methods=['GET', 'POST'])
def join_faculty():
    form = JoinFaculty()
    if request.method == 'POST' and form.validate():
        check_email = Teacher.query.filter_by(email=form.email.data).first()
        if check_email != None:
            flash('This email is already assigned to a Teacher. Are you sure you are not already a teacher at this school?')
            return render_template('teacher_templates/join_faculty.html', form=form)
        new_teacher = Teacher(first_name=form.first_name.data, last_name=form.last_name.data, started_at_school=form.started_at_school.data, pic_url=form.pic_url.data, email=form.email.data, password_hash=generate_password_hash(form.password.data))
        db.session.add(new_teacher)
        db.session.commit()
        flash(f'Thank you {new_teacher.first_name} {new_teacher.last_name}. You are now a registered teacher. Please Log in!')
        return redirect('/login')
    return render_template('teacher_templates/join_faculty.html', form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.email != os.environ['ADMIN1']:
        return render_template('alerts/access_denied.html')
    teachers = Teacher.query.all()
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('admin.html', teachers=teachers, students=students, courses=courses)

@app.route('/reset_password/<string:code>', methods=['GET', 'POST'])
def reset_password(code):
    if current_user.is_authenticated:
        flash('You are already logged in. If you want to change your password, you can do that in the Account Settings Tab.')
        return render_template('password_templates/reset_password.html')
    form = ResetPassword()
    user = Student.query.filter_by(reset_code=code).first()
    if user == None:
        user = Teacher.query.filter_by(reset_code=code).first()
    if user == None:
        return render_template('password_templates/reset_password.html', alert="This link in no longer active. Please click the link send to your email, or ask for a new one to be resent.")
    if form.validate_on_submit():
        new_hash = generate_password_hash(form.new_password.data)
        user.password_hash = new_hash
        db.session.commit()
        flash('Your Password has been updated. Please Login.')
        return redirect('/login')
    return render_template('password_templates/reset_password.html', code=code, user=user, form=form)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        flash('You are already logged in. If you want to change your password, you can do that in the Account Settings Tab.')
        return render_template('password_templates/forgot_password.html')
    form = ForgotPassword()
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.email.data).first()
        if user == None:
            user = Teacher.query.filter_by(email=form.email.data).first()
        if user == None:
            flash("Hmmm. This email doesn't seem to be registered at this highschool.")
            return render_template('password_templates/reset_password.html')
        code = secrets.token_hex(20)
        user.reset_code = code
        db.session.commit()
        # mail only works when debug mode is off. please make sure you are in production mode if you want the emails to work
        msg = Message(f"Hi {user.first_name}",
                    sender=os.environ['GMAIL_ACCOUNT'],
                    recipients=[user.email])
        msg.html = template1(user, code)
        mail.send(msg)
        flash('Please check your email. A link has been sent to you with a link to reset your password.')
        return redirect('/login')
    return render_template('password_templates/forgot_password.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('alerts/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('alerts/500.html'), 500
