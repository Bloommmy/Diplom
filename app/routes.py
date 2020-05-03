# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask import request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user
from app.models import User, Faculty, Department, Form_all, Degree, Direction, Profile, groupStud, Form_one, Form_two
from flask_login import logout_user
from flask_login import login_required
from app import db
from app.forms import RegistrationForm
import random
from app.forms import EditProfileForm
from app.forms import F_One
from app.forms import F_Two
from app.forms import F_Three
from app.forms import F_Four

@app.route('/')
@app.route('/index')
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

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Изменения успешно сохранены.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/fone/<username>', methods=['GET', 'POST'])
@login_required
def fone(username):
    user = User.query.filter_by(username=username).first_or_404()
    FacultyU = Faculty.query.get(user.Faculty_id)
    DepartmentU = Department.query.get(user.Department_id)
    Year = "Весна 2020"
    f=Form_all.query.order_by(Form_all.timestamp.desc()).first().id
    if f == None:
        num = 1
    else:
        num = f + 1

    form = F_One()
    if form.validate_on_submit():
        kol = Form_all.query.filter(Form_all.user_id == '1', Form_all.Status == None).count()
        if kol == 0:
            form1 = Form_all(user_id = user.id,
                            Faculty_id = FacultyU.abbreviation,
                            Department_id = DepartmentU.abbreviation,
                            Year = Year)
            db.session.add(form1)
            db.session.commit()
            numForm = Form_all.query.order_by(Form_all.timestamp.desc()).first().id
            g = 0
            return redirect(url_for('ftwo',
                                    username = current_user.username,
                                    numForm = numForm,
                                    g = g))

    return render_template('fone.html',
                            num = num,
                            FacultyU = FacultyU,
                            DepartmentU = DepartmentU,
                            Year = Year,
                            user = user,
                            form = form)

@app.route('/ftwo/<username>/<numForm>/<g>', methods=['GET', 'POST'])
@login_required
def ftwo(username, numForm, g):
    user = User.query.filter_by(username=username).first_or_404()
    FacultyU = Faculty.query.get(user.Faculty_id)
    DepartmentU = Department.query.get(user.Department_id)
    form = F_Two()
    def addForm_one():
        form2 = Form_one(NumForm = numForm,
                        Group_id = form.Group_id.data,
                        Degree_id = form.Degree_id.data,
                        Direction_id = form.Direction_id.data,
                        Direction_name = form.Direction_name.data,
                        Profile_id = form.Profile_id.data,
                        Profile_name = form.Profile_name.data,
                        Course = form.Course.data,
                        NumStudents = form.NumStudents.data)
        db.session.add(form2)
        db.session.commit()
        f=Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).first().Group_id
        g = f
        return g

    if form.validate_on_submit():
        if form.AddGroup.data == True: #добавление группы
            g = addForm_one()
            flash('Данные о группе успехно добавлены')
            return redirect(url_for('ftwo', username = current_user.username, numForm = numForm, g = g))
        elif form.SetUpForm.data == True:
            return redirect(url_for('fthree', username = current_user.username, numForm = numForm))
    elif request.method == 'GET':
        u = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).first()
        if u != None:
            form.Group_id.data = u.Group_id
            form.Degree_id.data = u.Degree_id
            form.Direction_id.data = u.Direction_id
            form.Direction_name.data = u.Direction_name
            form.Profile_id.data = u.Profile_id
            form.Profile_name.data = u.Profile_name
            form.Course.data = u.Course
            form.NumStudents.data = u.NumStudents
    g=int(g)
    if g != 0:
        items=Form_one.query.filter(Form_one.NumForm == numForm).all()
        return render_template('ftwo.html',
                                g = g,
                                numForm = numForm,
                                items = items,
                                form=form)
    else:
        return render_template('ftwo.html',
                                g = g,
                                numForm = numForm,
                                items = 0,
                                form=form)


@app.route('/fthree/<username>/<numForm>', methods=['GET', 'POST'])
@login_required
def fthree(username, numForm):

    form = F_Three()


    items=Form_one.query.filter(Form_one.NumForm == numForm).all()
    return render_template('fthree.html', numForm = numForm, items=items, form=form)

@app.route('/ffour/<username>/<numForm>/<group>', methods=['GET', 'POST'])
@login_required
def ffour(username, numForm, group):
    form = F_Four()
    if form.validate_on_submit():
        u = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == group).first()
        u.Group_id = form.Group_id.data
        u.Degree_id = form.Degree_id.data
        u.Direction_id = form.Direction_id.data
        u.Direction_name = form.Direction_name.data
        u.Profile_id = form.Profile_id.data
        u.Profile_name = form.Profile_name.data
        u.Course = form.Course.data
        u.NumStudents = form.NumStudents.data
        db.session.commit()
        flash('Изменения успешно сохранены.')
        return redirect(url_for('fthree', username = current_user.username, numForm = numForm))

    elif request.method == 'GET':
        u = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == group).first()
        form.Group_id.data = u.Group_id
        form.Degree_id.data = u.Degree_id
        form.Direction_id.data = u.Direction_id
        form.Direction_name.data = u.Direction_name
        form.Profile_id.data = u.Profile_id
        form.Profile_name.data = u.Profile_name
        form.Course.data = u.Course
        form.NumStudents.data = u.NumStudents
    return render_template('ffour.html', numForm = numForm, group = group, form=form)
