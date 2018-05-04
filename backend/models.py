from flask import Flask
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.TRACK_MODIFICATIONS

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))
    email = Column(String(length=120), unique=True)
    password = Column(String(length=50))
    school = Column(Integer) # this is the school id

    def __init__(self, first_name, last_name, email, password, school):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.school = school

    def __repr__(self):
        return '<email {}>'.format(self.email)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    grade = Column(String(length=5))
    credits = Column(Float)
    year = Column(Integer)
    transcript_id = Column(Integer)

    def __init__(self, name, grade, credits, year, tid):
        self.name = name
        self.grade = grade
        self.credits = credits
        self.year = year
        self.transcript_id = tid

class School(Base):
    __tablename__ = 'schools'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=500))
    email = Column(String(length=120), unique=True)
    password = Column(String(length=50))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class College(Base):
    __tablename__ = 'colleges'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=500))
    email = Column(String(length=120), unique=True)
    password = Column(String(length=50))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Transcript(Base):
    __tablename__ = 'transcript'

    id = Column(Integer, primary_key=True)
    student = Column(Integer)
    school = Column(Integer)

    _colleges = [] # append the id number here

    def __init__(self, student, school):
        self.student = student
        self.school = school
