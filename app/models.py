from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt
from app import app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    FullName = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    Faculty = db.Column(db.Integer)
    Department = db.Column(db.Integer)
    Phone = db.Column(db.String(12))
    access = db.Column(db.String)

    forms = db.relationship('Form_all', cascade='save-update, all, delete', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<FullName {}>'.format(self.FullName)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Form_all(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True, unique = True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Faculty = db.Column(db.String)
    Department = db.Column(db.String)
    Year = db.Column(db.String)
    Status = db.Column(db.String)

    form_one = db.relationship('Form_one', cascade='save-update, all, delete', backref='form_one', lazy='dynamic')
    form_two = db.relationship('Form_two', cascade='save-update, all, delete', backref='form_two', lazy='dynamic')

    def __repr__(self):
        return '<Form_all {}>'.format(self.id)


class Form_one(db.Model):
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    NumForm = db.Column(db.Integer, db.ForeignKey('form_all.id'), primary_key=True)
    Group_id = db.Column(db.Integer, primary_key=True)
    Degree_id = db.Column(db.Integer)
    Direction_id = db.Column(db.Integer)
    Direction_name = db.Column(db.String)
    Profile_id = db.Column(db.Integer)
    Profile_name = db.Column(db.String)
    Course = db.Column(db.Integer)
    NumStudents = db.Column(db.Integer)

    groups = db.relationship('Form_two', backref='groups', cascade='all, delete', lazy='dynamic')

    def __repr__(self):
        return '<Form_one {}>'.format(self.Group_id)

class Form_two(db.Model):
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    NumForm = db.Column(db.Integer, db.ForeignKey('form_all.id'), primary_key=True)
    Group_id = db.Column(db.Integer, db.ForeignKey('form_one.Group_id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    FullSubject = db.Column(db.String)
    BriefSubject = db.Column(db.String)
    LecturerName = db.Column(db.String)
    LecturerDepartment = db.Column(db.String)
    PracticianName = db.Column(db.String)
    PracticianDepartment = db.Column(db.String)
    course_work = db.Column(db.String)
    practice_work = db.Column(db.String)
    laboratory_work = db.Column(db.String)

    def __repr__(self):
        return '<Form_two {}>'.format(self.id)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#u = User(username='susan', FullName='Маркова Ольга Николаевна', email='susan@example.com', Faculty='КТИ', Department ='АПУ', Phone='+79992118773', access='admin')
