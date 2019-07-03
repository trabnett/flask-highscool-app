from flask_wtf import FlaskForm
from datetime import datetime, date
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo, Length, Regexp
from wtforms.widgets import PasswordInput

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class TestScore(FlaskForm):
    test_name = StringField('Test Name:', validators=[DataRequired()])
    student = StringField('Student', validators=[DataRequired()])
    score= IntegerField('Score', validators=[DataRequired(), NumberRange(min=0, max=100, message="You Must Enter A Value Between 0-100")])
    submit = SubmitField('Register Test Scores')

class NewSport(FlaskForm):
    sport_name = StringField('String Name', validators=[DataRequired()])
    max_size = IntegerField('Max Size', validators=[DataRequired()])
    submit = SubmitField('Submit New Team')

class NewCourse(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired()])
    grade = IntegerField('Grade', validators=[DataRequired(), NumberRange(min=9,max=12,message=('This school only offers grads 9-12.'))])
    submit = SubmitField('Create Course')

class Register(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d', default=date(2000, 1, 1))
    grade = IntegerField('Grade', validators=[DataRequired(), NumberRange(min=9,max=12,message=('This school only offers grads 9-12.'))])
    pic_url = StringField('Picture Url', validators=[DataRequired()])
    twitter = StringField('Twitter - (not required)', default=None)
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password',)
    submit = SubmitField('Register')

class JoinFaculty(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    started_at_school = DateField('Started At School', format='%Y-%m-%d', default=datetime.now())
    pic_url = StringField('Picture Url', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password',)
    submit = SubmitField('Register')

class ResetPassword(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), Regexp(r'^[\w.@+-]+$', message='Come on man. You know you cant use spaces in a password.'), Length(min=4), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Reset Password')

class ForgotPassword(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')