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

    form_all = db.relationship('Form_all', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<FullName {}>'.format(self.FullName)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Form_all(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True, unique = True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Faculty_id = db.Column(db.Integer)
    Department_id = db.Column(db.Integer)
    Year = db.Column(db.String)
    Status = db.Column(db.String)

    form_one = db.relationship('Form_one', backref='form_one', lazy='dynamic')
    form_two = db.relationship('Form_two', backref='form_two', lazy='dynamic')

    def __repr__(self):
        return '<Form_all {}>'.format(self.id)


class Form_one(db.Model):
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    NumForm = db.Column(db.Integer, db.ForeignKey('form_all.id'), primary_key=True)
    Group_id = db.Column(db.Integer, primary_key=True, index=True, unique = True)
    Degree_id = db.Column(db.Integer)
    Direction_id = db.Column(db.Integer, db.ForeignKey('direction.id'))
    Direction_name = db.Column(db.String)
    Profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    Profile_name = db.Column(db.String)
    Course = db.Column(db.Integer)
    NumStudents = db.Column(db.Integer)


    Direction = db.relationship('Direction', backref='form_one')
    Profile = db.relationship('Profile', backref='form_one')


    def __repr__(self):
        return '<Form_one {}>'.format(self.Group_id)

class Form_two(db.Model):
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    NumForm = db.Column(db.Integer, db.ForeignKey('form_all.id'), primary_key=True)
    Group_id = db.Column(db.Integer, db.ForeignKey('form_one.Group_id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True, index=True, unique = True)

    FullSubject = db.Column(db.String)
    ВriefSubject = db.Column(db.String)

    LecturerName = db.Column(db.String)
    LecturerDepartment = db.Column(db.String)

    PracticianName = db.Column(db.String)
    PracticianDepartment = db.Column(db.String)

    course_work = db.Column(db.String)
    practice_work = db.Column(db.String)
    laboratory_work = db.Column(db.String)

    Group = db.relationship('Form_one', backref='form_two')

    def __repr__(self):
        return '<Form_two {}>'.format(self.id)


class Faculty(db.Model): #ФАКУЛЬТЕТ
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String)
    name = db.Column(db.String)
    Department = db.relationship('Department', backref='faculty', lazy='dynamic')

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

class Degree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


    def __repr__(self):
        return '<Degree {}>'.format(self.name)

class Direction(db.Model):
    Faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    Degree_id = db.Column(db.Integer, db.ForeignKey('degree.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    Degree = db.relationship('Degree', backref='direction')
    Faculty = db.relationship('Faculty', backref='direction')

    def __repr__(self):
        return '<Direction {}>'.format(self.name)

class Profile(db.Model):
    Direction_id = db.Column(db.Integer, db.ForeignKey('direction.id'))
    Department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    Direction = db.relationship('Direction', backref='profile')
    Department = db.relationship('Department', backref='profile')

    def __repr__(self):
        return '<Profile {}>'.format(self.name)

class groupStud(db.Model):
    Profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    Profile = db.relationship('Profile', backref='groupStud')

    def __repr__(self):
        return '<groupStud {}>'.format(self.id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#u = User(username='susan', FullName='Маркова Ольга Николаевна', email='susan@example.com', Faculty_id=1, Department_id =1, Phone='+79992118773', access='admin')
