# Welcome to Tim Rabnett High School
## A simulated highschool website created using Flask and Postgres.
##### This project uses many common features of Flask, Postgres and Flask-Bootstrap. 



webapp is hosted on heroku at:
[TRHS webapp](https://trhs.herokuapp.com/)


#### employs:

+ Flask
+ Flask-Bootstrap for styling
+ WTForms for forms
+ Flask-Login user authentication
+ Flask-Mail for resetting forgotten passwords
+ Scripting with Javascript and jQuery

#### Quick Start
1. Clone the repo
``
 $ git clone https://github.com/trabnett/flask-highscool-app
``
``
 $ cd flask-highschool-app
``

2. Initialize and activate a virtualenv
``
$ virtualenv venv
``
``
$ source venv/bin/activate
``
3. Install dependencies
``
$ pip install -r requirements.txt
``
4. Configure .env file
``
copy the example of the .envexample file
``
5. Run the development server  
``
flask run
``

The main purposes of this app were to create relational data between students and teachers using SQLAlchemy and to practice responsive layouts. 

## Screenshots
### Some features include:

Front page with parallax scrolling with fade

![Front Page](https://github.com/trabnett/flask-highscool-app/blob/master/app/static/img/homepage.gif)

Responsive Student page that summarizes academic performance

![Student Page](https://github.com/trabnett/flask-highscool-app/blob/master/app/static/img/student.gif)

Teacher page allows teachers to enter new test scores and remove or add Students from Courses

![Teacher Page](https://github.com/trabnett/flask-highscool-app/blob/master/app/static/img/teacher.gif)

Responsive view displays well on most mobile devices (no fixed background pictures on iOS devices)

![Mobile View Page](https://github.com/trabnett/flask-highscool-app/blob/master/app/static/img/mobile.gif)