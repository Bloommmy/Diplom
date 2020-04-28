# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask import request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user
from app.models import User, Faculty, Department, Form
from flask_login import logout_user
from flask_login import login_required
from app import db
from app.forms import RegistrationForm
import random

@app.route('/')
@app.route('/index')
#@login_required
def index():
    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/PersonalArea/<username>')
@login_required
def PersonalArea(username):
    user = User.query.filter_by(username=username).first_or_404()
    FacultyN = Faculty.query.get(user.Faculty_id)
    DepartmentN = Department.query.get(user.Department_id)
    return render_template('PersonalArea.html', user=user, FacultyN=FacultyN, DepartmentN=DepartmentN, title='PersonalArea')

@app.route('/register', methods=['GET', 'POST'])
def register():
    def generation():
        chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        number = 1
        length = 5
        for n in range(number):
            new =''
            for i in range(length):
                new += random.choice(chars)
        return new
    form = RegistrationForm(request.form)
    form.Faculty_id.choices = [(d.id, d.name) for d in Faculty.query.all()]
    #form = UserDetails(request.POST, obj=user)
    form.Department_id.choices = [(d.id, d.name) for d in Department.query.all()]

    if form.validate_on_submit():
        username = generation()
        user = User.query.filter_by(username=username).first()
        while user is not None:
            username = generation()
            user = User.query.filter_by(username=username).first()

        user = User(username=username, FullName=form.FullName.data, email=form.email.data, Faculty_id=form.Faculty_id.data, Department_id=form.Department_id.data, Phone=form.Phone.data, access=form.access.data)
        password = generation()

        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return render_template('RegistrationTotal.html', username=username, password=password, title='RegistrationTotal')
    return render_template('register.html', title='Register', form=form)
