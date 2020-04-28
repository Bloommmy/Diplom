from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    FullName = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    Faculty_id = db.Column(db.Integer)
    Department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    Phone = db.Column(db.String(12))
    access = db.Column(db.String)
    Forms = db.relationship('Form', backref='author', lazy='dynamic')



    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Faculty_id = db.Column(db.Integer)
    Faculty = db.Column(db.String)
    Department_id = db.Column(db.Integer)
    Department = db.Column(db.String)
    Degree_id = db.Column(db.Integer)
    Degree = db.Column(db.String)
    Year = db.Column(db.String)
    Direction_id = db.Column(db.Integer)
    Direction = db.Column(db.String)
    Profile_id = db.Column(db.Integer)
    Profile = db.Column(db.String)
    Course = db.Column(db.Integer)
    Group_id = db.Column(db.Integer)
    NumStudents = db.Column(db.Integer)


    def __repr__(self):
        return '<Form {}>'.format(self.id)

class Faculty(db.Model): #ФАКУЛЬТЕТ
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String)
    name = db.Column(db.String)
    Department = db.relationship('Department', backref='department', lazy='dynamic')

    def __repr__(self):
        return '<Faculty {}>'.format(self.name)

class Department(db.Model): # КАФЕДРА
    Faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String)
    name = db.Column(db.String)
    workers = db.relationship('User', backref='worker', lazy='dynamic')

    def __repr__(self):
        return '<Department {}>'.format(self.name)

'''class Direction(db.Model): #НАПРАВЛЕНИЕ
    Department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    Degree_id = db.Column(db.Integer, db.ForeignKey('degree.id'))
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String)
    name = db.Column(db.String)
    profile = db.relationship('Profile', backref='profile', lazy='dynamic')

    def __repr__(self):
        return '<Direction {}>'.format(self.name)

class Degree(db.Model): #КЛАССИФМКАЦИЯ: БАКАЛАВРЫ МАГИСТРЫ и ТД
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    direction = db.relationship('Direction', backref='direction', lazy='dynamic')

    def __repr__(self):
        return '<Degree {}>'.format(self.name)

class Profile(db.Model):
    Department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    Direction_id = db.Column(db.Integer, db.ForeignKey('direction.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Profile {}>'.format(self.name)'''

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#u = User(username='susan', FullName='Маркова Ольга Николаевна', email='susan@example.com', Faculty_id=1, Department_id =1, Phone='+79992118773', access='admin')
