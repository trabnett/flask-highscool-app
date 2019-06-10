from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
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