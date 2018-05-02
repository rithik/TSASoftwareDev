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

def log(msg):
    if settings.PRODUCTION:
        pass
    else:
        print(msg, file=sys.stderr)

@app.route('/')
def home_page():
    return "Home Page"

@app.route('/school/<school_id>/register/student')
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

@app.route('/register/school')
def create_school():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        address = request.form["address"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if not confirm_password == password:
            return redirect(url_for('.home_page'))
        new_school = School(name, email, address, password)
        db_session.add(new_school)
        db_session.commit()
        log('School Created')
        return redirect(url_for('.home_page'))

@app.route('/register/college')
def create_college():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if not confirm_password == password:
            return redirect(url_for('.home_page'))
        new_college = College(name, email, password)
        db_session.add(new_college)
        db_session.commit()
        log('College Created')
        return redirect(url_for('.home_page'))

@app.route('/school/<school_id>/student/<student_id>')
def create_college():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if not confirm_password == password:
            return redirect(url_for('.home_page'))
        new_college = College(name, email, password)
        db_session.add(new_college)
        db_session.commit()
        log('College Created')
        return redirect(url_for('.home_page'))


if __name__ == '__main__':
    app.run()
