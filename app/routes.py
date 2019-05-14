from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.students import Students

enrolledStudents = Students()
print(enrolledStudents[0]['name'])

@app.route('/')
def welcome():
    user = {'username': 'Tim'}
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/students')
def students():
    return render_template('students.html', students=enrolledStudents)

@app.route('/student/<string:id>')
def student(id):
    kid = {'alert': 'this student is not registered'}
    for student in enrolledStudents:
        if int(student['id']) == int(id):
            print('Yea!!')
            kid = student
    return render_template('student.html', student=kid)