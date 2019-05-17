from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.students import Students
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import Student, Teacher, StudentCourse, Course

teacher = {'status': True}

@app.route('/')
def welcome():
    user = {'username': 'Tim'}
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(current_user, "right at the start of login ==================")
    if current_user.is_authenticated and current_user.birthday:
        teacher['status'] = False
        return redirect(f'/student/{current_user.id}')
    if current_user.is_authenticated and current_user.started_at_school:
        return redirect(url_for('welcome'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.username.data).first()
        if user == None:
            user = Teacher.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print("nooo")
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        if hasattr(user, 'birthday'):
            teacher['status'] = False
            print(teacher, "in routes.py")
            return redirect(f'/student/{user.id}')
        if hasattr(user, 'started_at_school'):
            teacher['status'] = True
            print(teacher, "in routes.py")
            return redirect(url_for('welcome'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/students')
def students():
    enrolledStudents = Student.query.all()
    print(enrolledStudents)
    return render_template('students.html', students=enrolledStudents)

@app.route('/student/<string:id>')
def student(id):
    kid = {'alert': 'this student is not registered'}
    enrolledStudents = Student.query.all()
    for student in enrolledStudents:
        if int(student.id) == int(id):
            kid = student
    return render_template('student.html', student=kid)