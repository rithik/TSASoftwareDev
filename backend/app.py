from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from models import Student, Course, School, College, Transcript
import settings
import sys
from database import db_session
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['APP_SETTINGS'] = settings.APP_SETTINGS
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.TRACK_MODIFICATIONS
app.secret_key = settings.SECRET_KEY


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def log(msg):
    if settings.PRODUCTION:
        pass
    else:
        print(msg, file=sys.stderr)

@app.route('/signout', methods=["GET", "POST"])
def signout():
    db_session.pop('type', None)
    session.pop('user', None)
    return redirect("/")

@app.route('/', methods=["GET", "POST"])
def home_page():
    if request.method == "GET":
        t = session.get('type', {})
        u = session.get('user', {})
        try:
            if t == 'student':
                return redirect("/transcript/" + u)
            elif t == 'school':
                return redirect("/school/" + u)
            elif t == 'college':
                return redirect("/college/" + u)
        except:
            pass
        return render_template('welcome.html')

@app.route('/school/<school_id>/register/student', methods=["GET", "POST"])
def create_student(school_id): # Students must be registered through their school
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if not email.index("@") > 0 and not email.index(".") > email.index("@"):
            return redirect(url_for('.home_page'))
        if not confirm_password == password:
            return redirect(url_for('.home_page'))
        u = Student.query.filter_by(email=email).count()
        if u == 0:
            new_student = Student(first_name, last_name, email, password, int(school_id))
            db_session.add(new_student)
            db_session.commit()
            log('Student Created')
            return redirect(url_for('.home_page'))
        return redirect(url_for('.home_page'))
    if request.method == "GET":
        return render_template('student_register.html')

@app.route('/register', methods=["GET", "POST"])
def create_inst():
    if request.method == "GET":
        return render_template('register.html')
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        option = request.form['option']
        if not confirm_password == password:
            return redirect(url_for('.home_page'))
        if option == 'school':
            new_school = School(name, email, password)
            db_session.add(new_school)
            db_session.commit()
            log('School created')
        elif option == 'college':
            new_college = College(name, email, password)
            db_session.add(new_college)
            db_session.commit()
            log('College Created')
        return redirect(url_for('.home_page'))

@app.route('/login', methods=["GET", "POST"])
def login_method():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        s = Student.query.filter_by(email=email).count()
        if not s == 0:
            student = Student.query.filter_by(email=email).first()
            if password == student.password:
                session['user'] = student.id
                session['type'] = 'student'
                return redirect(url_for('.view_transcript'))
        sch = School.query.filter_by(email=email).count()
        if not sch == 0:
            school = School.query.filter_by(email=email).first()
            if password == school.password:
                session['user'] = school.id
                session['type'] = 'school'
                return redirect('/school/' + school.id)
        col = College.query.filter_by(email=email).count()
        if not col == 0:
            college = College.query.filter_by(email=email).first()
            if password == College.password:
                session['user'] = college.id
                session['type'] = 'college'
                return redirect('/college/' + college.id)
        return "Error: Invalid Login"
    if request.method == "GET":
        return render_template('login.html')

@app.route('/school/<school_id>', methods=["GET", "POST"])
def school_page(school_id):
    if request.method == "GET":
        t = session.get('type', {})
        u = session.get('user', {})
        if int(school_id) == int(u) and t == 'school':
            school = School.query.filter_by(id=int(school_id)).first()
            d = {}
            for k in school.transcripts:
                d[k.id] = k.student.first_name + " " + k.student.last_name
            return render_template('school.html', transcripts=d)
        else:
            return 'Error: Not Authorized'

@app.route('/college/<college_id>', methods=["GET", "POST"])
def college_page(college_id):
    if request.method == "GET":
        t = session.get('type', {})
        u = session.get('user', {})
        if int(college_id) == int(u) and t == 'college':
            college = College.query.filter_by(id=int(college_id)).first()
            d = {}
            for k in college.transcripts:
                d[k.id] = k.student.first_name + " " + k.student.last_name
            return render_template('college.html', transcripts=d)
        else:
            return 'Error: Not Authorized'

@app.route('/transcript/<tid>/add', methods=["GET", "POST"])
def add_course(tid):
    if request.method == "POST":
        t = Transcript.query.filter_by(id=int(tid)).first()
        t = session.get('type', {})
        u = session.get('user', {})
        if t.school.id == int(u) and t == 'school':
            course_name = request.form["name"]
            grade = request.form["grade"]
            credits = float(request.form["credits"])
            year = int(request.form["year"])
            new_course = Course(name, grade, credits, year)
            db_session.add(new_course)
            db_session.commit()
            log('Added Course')
        return redirect(url_for('.view_transcript'))
    if request.method == "GET":
        return render_template('add_course.html')

@app.route('/transcript/<tid>', methods=["GET", "POST"])
def view_transcript(tid):
    if request.method == "GET":
        t = Transcript.query.filter_by(id=int(tid)).first()
        t = session.get('type', {})
        u = session.get('user', {})
        if t.student.id == int(u) or t.school.id == int(u):
            courses = t.courses
            return render_template('transcript.html', courses=courses)
        q = []
        for x in t.colleges:
            q.append(x.id)
        if int(u) in q:
            courses = t.courses
            return render_template('transcript.html', courses=courses)
        return "Error: Not Authorized"

@app.route('/transcript/<tid>/add_college', methods=["GET", "POST"])
def add_college(tid):
    if request.method == "POST":
        t = Transcript.query.filter_by(id=int(tid)).first()
        t = session.get('type', {})
        u = session.get('user', {})
        if t.student.id == int(u):
            cid = request.form['college_id']
            c = College.query.filter_by(id=int(cid)).first()
            t.colleges.append(c)
            db_session.add(t)
            db_session.commit()
            return redirect(url_for('.view_transcript'))
        return "Error: Not Authorized"
    if request.method == "GET":
        return render_template('add_college.html')

if __name__ == '__main__':
    app.run()
