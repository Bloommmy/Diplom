# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask import request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user
from app.models import User, Form_all, Form_one, Form_two
from flask_login import logout_user
from flask_login import login_required
from app import db
from app.forms import RegistrationForm
import random
from app.forms import EditProfileForm
from app.forms import F_One
from app.forms import F_One_edit
from app.forms import F_Two
from app.forms import F_Two_edit

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
    FacultyN = user.Faculty
    DepartmentN = user.Department
    return render_template('PersonalArea.html', user=user, FacultyN=FacultyN, DepartmentN=DepartmentN, title='PersonalArea')

@app.route('/register', methods=['GET', 'POST'])
@login_required
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

    if form.validate_on_submit():
        username = generation()
        user = User.query.filter_by(username=username).first()
        while user is not None:
            username = generation()
            user = User.query.filter_by(username=username).first()

        user = User(username=username, FullName=form.FullName.data, email=form.email.data, Faculty=form.Faculty.data, Department=form.Department.data, Phone=form.Phone.data, access=form.access.data)
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
        flash('Изменения успешно сохранены')
        return redirect(url_for('PersonalArea', username = current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/form0/<username>/<i>', methods=['GET', 'POST'])
@login_required
def form0(username, i):
    def check(f1):
        if f1 != 0:
            f1 = Form_one.query.filter(Form_one.NumForm == numForm).all()

            items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
            items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()


            items1_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 1).count()
            if items1_1 != 0:
                items1_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 1).all()
            else:
                items1_1=0

            items1_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 2).count()
            if items1_2 != 0:
                items1_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 2).all()
            else:
                items1_2=0

            items1_3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 3).count()
            if items1_3 != 0:
                items1_3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 3).all()
            else:
                items1_3=0

            items1_4=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 4).count()
            if items1_4 != 0:
                items1_4=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 4).all()
            else:
                items1_4=0

            items2_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 1).count()
            if items2_1 != 0:
                items2_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 1).all()
            else:
                items2_1=0

            items2_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 2).count()
            if items2_2 != 0:
                items2_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 2).all()
            else:
                items2_2=0

            f2 = Form_two.query.filter(Form_two.NumForm == numForm).count()
            if f2 != 0:
                f2 = Form_two.query.filter(Form_two.NumForm == numForm).all()
            else:
                f2 = 0
        else:
            f1 = 0
            items1 = 0
            items2 = 0
            items1_1 = 0
            items1_2 = 0
            items1_3 = 0
            items1_4 = 0
            items2_1 = 0
            items2_2 = 0
            f2 = 0
        return (f1, items1_1, items1_2, items1_3, items1_4, items2_1, items2_2, f2, items1, items2)

    user = User.query.filter_by(username=username).first_or_404()
    Faculty = user.Faculty
    Department = user.Department
    Year = "весна 2020"

    #Проверка на наличие незаконченных заявок
    f0 = Form_all.query.filter(Form_all.user_id == user.id, Form_all.Status == None).count()
    if f0 != 0: #Если есть незаконченные заявки
        f0 = Form_all.query.filter(Form_all.user_id == user.id, Form_all.Status == None).first()
        numForm = f0.id  #Выясняем номер заявки
        f1 = Form_one.query.filter(Form_one.NumForm == numForm).count()
        f1,items1_1,items1_2,items1_3,items1_4,items2_1,items2_2,f2, items1, items2 = check(f1)
        koll = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).count() #Узнаем количество групп в заявке
        groups = Form_one.query.filter(Form_one.NumForm == numForm).all() #Узнаем номера групп
        G = []

        for i in groups:
            G.append(i.Group_id)
        items=Form_two
        return render_template('form0.html',
                                numForm = numForm,
                                Faculty = 0,
                                Department = 0,
                                Year = 0,
                                user = user,
                                f0 = f0, f1 = f1, f2 = f2,
                                items1_1 = items1_1, items1_2 = items1_2,
                                items1_3 = items1_3, items1_4 = items1_4,
                                items2_1 = items2_1, items2_2 = items2_2,
                                items1 = items1, items2 = items2,
                                koll = koll, G = G, items = items)



    elif f0 == 0:
        f=Form_all.query.order_by(Form_all.timestamp.desc()).count()
        if f == 0:
            numForm = 1
        else:
            f=Form_all.query.order_by(Form_all.timestamp.desc()).first().id
            numForm = f + 1
        form0 = Form_all(user_id = user.id,
                        Faculty = Faculty,
                        Department = Department,
                        Year = Year)
        db.session.add(form0)
        db.session.commit()
        numForm = Form_all.query.order_by(Form_all.timestamp.desc()).first().id
        return render_template('form0.html',
                                f0 = 0,
                                numForm = numForm,
                                Faculty = Faculty,
                                Department = Department,
                                Year = Year,
                                user = user, i=i)

@app.route('/form_delet/<username>/<numForm>/<i>/<g>')
@login_required
def form_delet(username, numForm, i, g):
    user = User.query.filter_by(username=username).first_or_404()
    if i == '1':
        f = Form_all.query.get(numForm)
        db.session.delete(f)
        db.session.commit()
        flash('Заявка {} успешно удалена'.format(numForm))
        return redirect(url_for('index'))
    elif i == '2':
        f = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == g).first()
        db.session.delete(f)
        db.session.commit()
        flash('Группа {} успешно удалена'.format(g))
        return redirect(url_for('form12_promo', username = current_user.username, numForm = numForm))
    elif i == '3':
        f = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == g).first()
        db.session.delete(f)
        db.session.commit()
        flash('Группа {} успешно удалена'.format(g))
        return redirect(url_for('form1_promo', username = current_user.username, numForm = numForm))
    elif i == '4':
        f = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == g).first()
        db.session.delete(f)
        db.session.commit()
        flash('Группа {} успешно удалена'.format(g))
        return redirect(url_for('form0_edit', username = current_user.username, numForm = numForm))



@app.route('/form0_edit/<username>/<numForm>')
@login_required
def form0_edit(username, numForm):
    user = User.query.filter_by(username=username).first_or_404()
    def check(f1):
        if f1 != 0:
            f1 = Form_one.query.filter(Form_one.NumForm == numForm).all()

            items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
            items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()

            items1_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 1).count()
            if items1_1 != 0:
                items1_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 1).all()
            else:
                items1_1=0

            items1_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 2).count()
            if items1_2 != 0:
                items1_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 2).all()
            else:
                items1_2=0

            items1_3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 3).count()
            if items1_3 != 0:
                items1_3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 3).all()
            else:
                items1_3=0

            items1_4=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 4).count()
            if items1_4 != 0:
                items1_4=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 4).all()
            else:
                items1_4=0

            items2_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 1).count()
            if items2_1 != 0:
                items2_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 1).all()
            else:
                items2_1=0

            items2_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 2).count()
            if items2_2 != 0:
                items2_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 2).all()
            else:
                items2_2=0

            f2 = Form_two.query.filter(Form_two.NumForm == numForm).count()
            if f2 != 0:
                f2 = Form_two.query.filter(Form_two.NumForm == numForm).all()
            else:
                f2 = 0
        else:
            f1 = 0
            f2 = 0
            items1 = 0
            items2 = 0
            items1_1 = 0
            items1_2 = 0
            items1_3 = 0
            items1_4 = 0
            items2_1 = 0
            items2_2 = 0

        return (f1, f2, items1, items2, items1_1, items1_2, items1_3, items1_4, items2_1, items2_2)

    f0 = Form_all.query.filter(Form_all.user_id == user.id, Form_all.id == numForm).first()
    f1 = Form_one.query.filter(Form_one.NumForm == numForm).count()
    f1, f2, items1, items2, items1_1, items1_2, items1_3, items1_4, items2_1, items2_2 = check(f1)
    if f2 == 0:
        koll = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).count() #Узнаем количество групп в заявке
        groups = Form_one.query.filter(Form_one.NumForm == numForm).all() #Узнаем номера групп
        G = []

        for i in groups:
            G.append(i.Group_id) #записываем группы в массив

        all_g_ok = [0] * int(koll) #создаем нулевой массив равный количеству групп
        k = 0
        for i in range(int(koll)):
            items=Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == G[i]).count()
            if items != 0:
                all_g_ok[i] = G[i]
                k = k + 1
            else:
                 break
        items=Form_two

    else:
        G = 0
        koll = 0
        k = 0
        items = 0

    return render_template('form0_edit.html',
                            numForm = numForm,
                            user = user, G = G, koll = koll, items = items,
                            f0 = f0, f1 = f1, f2 = f2,
                            items1 = items1, items2 = items2,
                            items1_1 = items1_1, items1_2 = items1_2,
                            items1_3 = items1_3, items1_4 = items1_4,
                            items2_1 = items2_1, items2_2 = items2_2)

@app.route('/ftwo/<username>/<numForm>/<g>/<i>', methods=['GET', 'POST'])
@login_required
def form1(username, numForm, g, i):
    user = User.query.filter_by(username=username).first_or_404()
    FacultyU = user.Faculty
    DepartmentU = user.Department
    form = F_One()
    def addForm_one():
        form1 = Form_one(NumForm = numForm,
                        Group_id = form.Group_id.data,
                        Degree_id = form.Degree_id.data,
                        Direction_id = form.Direction_id.data,
                        Direction_name = form.Direction_name.data,
                        Profile_id = form.Profile_id.data,
                        Profile_name = form.Profile_name.data,
                        Course = form.Course.data,
                        NumStudents = form.NumStudents.data)
        db.session.add(form1)
        db.session.commit()
        f=Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).first().Group_id
        g = f
        return g

    if form.validate_on_submit():
        if form.AddGroup.data == True: #добавление группы
            if i == '1':
                g = addForm_one()
                flash('Данные о группе {} успехно добавлены'.format(g))
                return redirect(url_for('form1', username = current_user.username, numForm = numForm, g = g, i = i))
            elif i == '2':
                g = addForm_one()
                flash('Данные о группе {} успехно добавлены'.format(g))
                return redirect(url_for('form2', username=current_user.username, numForm=numForm, g=g, sub=0, p=0, i=i))
        elif form.SetUpForm.data == True:
            return redirect(url_for('form1_promo', username = current_user.username, numForm = numForm))
    elif request.method == 'GET':
        u = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).first()
        if u != None:
            form.Group_id.data = u.Group_id
            form.Degree_id.data = str(u.Degree_id)
            form.Direction_id.data = u.Direction_id
            form.Direction_name.data = u.Direction_name
            form.Profile_id.data = u.Profile_id
            form.Profile_name.data = u.Profile_name
            form.Course.data = u.Course
            form.NumStudents.data = u.NumStudents



    g=int(g)
    if g != 0 and i == '1':
        items1_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 1).count()
        if items1_1 != 0:
            items1_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 1).all()
        else:
            items1_1=0

        items1_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 2).count()
        if items1_2 != 0:
            items1_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 2).all()
        else:
            items1_2=0

        items1_3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 3).count()
        if items1_3 != 0:
            items1_3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 3).all()
        else:
            items1_3=0

        items1_4=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 4).count()
        if items1_4 != 0:
            items1_4=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 4).all()
        else:
            items1_4=0

        items2_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 1).count()
        if items2_1 != 0:
            items2_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 1).all()
        else:
            items2_1=0

        items2_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 2).count()
        if items2_2 != 0:
            items2_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 2).all()
        else:
            items2_2=0

        items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
        items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()

        return render_template('form1.html',
                                numForm = numForm, items = 1, items1 = items1, items2 = items2,
                                items2_1 = items2_1, items2_2 = items2_2,
                                items1_1 = items1_1, items1_2 = items1_2,
                                items1_3 = items1_3, items1_4 = items1_4,
                                g = g, form=form, i=i)

    elif i == '2':

        return render_template('form1.html',
                                g = g,
                                numForm = numForm,
                                items = 0, i=i,
                                form=form)
    else:
        return render_template('form1.html',
                                g = g,
                                numForm = numForm,
                                items = 0, i=i,
                                form=form)

@app.route('/form1_promo/<username>/<numForm>', methods=['GET', 'POST'])
@login_required
def form1_promo(username, numForm):
    items1_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 1).count()
    if items1_1 != 0:
        items1_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 1).all()
    else:
        items1_1=0

    items1_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 2).count()
    if items1_2 != 0:
        items1_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 2).all()
    else:
        items1_2=0

    items1_3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 3).count()
    if items1_3 != 0:
        items1_3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 3).all()
    else:
        items1_3=0

    items1_4=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 4).count()
    if items1_4 != 0:
        items1_4=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 4).all()
    else:
        items1_4=0

    items2_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 1).count()
    if items2_1 != 0:
        items2_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 1).all()
    else:
        items2_1=0

    items2_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 2).count()
    if items2_2 != 0:
        items2_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 2).all()
    else:
        items2_2=0

    items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
    items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()

    return render_template('form1_promo.html',
                            numForm = numForm, items = 1, items1 = items1, items2 = items2,
                            items2_1 = items2_1, items2_2 = items2_2,
                            items1_1 = items1_1, items1_2 = items1_2,
                            items1_3 = items1_3, items1_4 = items1_4)

@app.route('/form1_edit/<username>/<numForm>/<group>/<i>', methods=['GET', 'POST'])
@login_required
def form1_edit(username, numForm, group, i):
    form = F_One_edit()
    if form.validate_on_submit():
        def two():
            f = Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == group).count()
            if f != 0:
                f = Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == group).all()
                for i in f:
                    i.Group_id = form.Group_id.data
                    db.session.commit()
                    return(1)
            else:
                f = 0
                return(0)

        u = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == group).first()
        u.Group_id = form.Group_id.data
        u.Degree_id = form.Degree_id.data
        u.Direction_id = form.Direction_id.data
        u.Direction_name = form.Direction_name.data
        u.Profile_id = form.Profile_id.data
        u.Profile_name = form.Profile_name.data
        u.Course = form.Course.data
        u.NumStudents = form.NumStudents.data
        u1 = two()
        db.session.commit()
        flash('Изменения в группе {} успешно сохранены'.format(form.Group_id.data))
        if i == '1':
            return redirect(url_for('form1_promo', username = current_user.username, numForm = numForm))
        elif i == '2':
            return redirect(url_for('form12_promo', username = current_user.username, numForm = numForm))
        elif i == '3':
            return redirect(url_for('form0_edit', username = current_user.username, numForm = numForm))

    elif request.method == 'GET':
        u = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == group).first()
        form.Degree_id.data = str(u.Degree_id)
        form.Group_id.data = u.Group_id
        form.Direction_id.data = u.Direction_id
        form.Direction_name.data = u.Direction_name
        form.Profile_id.data = u.Profile_id
        form.Profile_name.data = u.Profile_name
        form.Course.data = u.Course
        form.NumStudents.data = u.NumStudents
    return render_template('form1_edit.html', numForm = numForm, group = group, form=form)

@app.route('/form2/<username>/<numForm>/<g>/<sub>/<p>/<i>', methods=['GET', 'POST'])
@login_required
def form2(username, numForm, g, sub, p, i):
    koll = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).count() #Узнаем количество групп в заявке
    kol = int(koll)-1
    groups = Form_one.query.filter(Form_one.NumForm == numForm).all() #Узнаем номера групп
    G = []
    p = int(p)
    for i in groups:
        G.append(i.Group_id)
    g = G[p]
    form = F_Two()


    def addForm_two(g):
        g = str(g)

        f=Form_two.query.filter(Form_two.NumForm == numForm).order_by(Form_two.timestamp.desc()).count()
        if f == 0:
            sub = 1
        else:
            f=Form_two.query.filter(Form_two.NumForm == numForm).order_by(Form_two.timestamp.desc()).first().id
            sub = int(f) + 1

        form2 = Form_two(NumForm = numForm,
                        Group_id = g,
                        id = sub,
                        FullSubject = form.FullSubject.data,
                        BriefSubject = form.BriefSubject.data,
                        LecturerName = form.LecturerName.data,
                        LecturerDepartment = form.LecturerDepartment.data,
                        PracticianName = form.PracticianName.data,
                        PracticianDepartment = form.PracticianDepartment.data,
                        course_work = form.course_work.data,
                        practice_work = form.practice_work.data,
                        laboratory_work = form.laboratory_work.data)
        db.session.add(form2)
        db.session.commit()
        return sub

    if form.validate_on_submit(): #добавление дисциплины
        sub = addForm_two(g)
        flash('Дисциплина успешно добавленна')
        return redirect(url_for('form2',
                                username = current_user.username,
                                numForm = numForm, g = g, sub = int(sub), p=p, i=i))

    elif request.method == 'GET':
        g = G[int(p)]
        u = Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == g).order_by(Form_two.timestamp.desc()).first()
        if u != None:
            form.FullSubject.data = u.FullSubject
            form.BriefSubject.data = u.BriefSubject
            form.LecturerName.data = u.LecturerName
            form.LecturerDepartment.data = u.LecturerDepartment
            form.PracticianName.data = u.PracticianName
            form.PracticianDepartment.data = u.PracticianDepartment
            form.course_work.data = u.course_work
            form.practice_work.data = u.practice_work
            form.laboratory_work.data = u.laboratory_work

    f=Form_two.query.filter(Form_two.NumForm == numForm).order_by(Form_two.timestamp.desc()).count()
    all_g_ok = [0] * int(koll)
    k = 0
    for i in range(int(koll)):
        items=Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == G[i]).count()
        if items != 0:
            all_g_ok[i] = G[i]
            k = k + 1
        else:
             break

    items=Form_two

    if f != 0:
        items=Form_two
        return render_template('form2.html', g = g, p = p, sub = int(sub), kol=kol, koll=koll, numForm = numForm, items = items, all_g = G, all_g_ok = all_g_ok, k=k, i=i, form=form)
    else:
        return render_template('form2.html', g = g, p = p, sub = int(sub), kol=kol, koll=koll, numForm = numForm, items = 0, all_g = G, all_g_ok = all_g_ok, k=k, i=i, form=form)

@app.route('/form2_edit/<username>/<numForm>/<group>/<sub>/<i>', methods=['GET', 'POST'])
@login_required
def form2_edit(username, numForm, group, sub, i):
    form = F_Two_edit()
    if form.validate_on_submit():
        u = Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == group, Form_two.id == sub).first()
        u.FullSubject = form.FullSubject.data
        u.BriefSubject = form.BriefSubject.data
        u.LecturerName = form.LecturerName.data
        u.LecturerDepartment = form.LecturerDepartment.data
        u.PracticianName = form.PracticianName.data
        u.PracticianDepartment = form.PracticianDepartment.data
        u.course_work = form.course_work.data
        u.practice_work = form.practice_work.data
        u.laboratory_work = form.laboratory_work.data
        db.session.commit()
        flash('Изменения успешно сохранены.')
        if i == '1':
            return redirect(url_for('form0_edit', username = current_user.username, numForm = numForm))
        elif i == '2':
            return redirect(url_for('form12_promo', username = current_user.username, numForm = numForm))

    elif request.method == 'GET':
        u = Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == group, Form_two.id == sub).first()
        form.FullSubject.data = u.FullSubject
        form.BriefSubject.data = u.BriefSubject
        form.LecturerName.data = u.LecturerName
        form.LecturerDepartment.data = u.LecturerDepartment
        form.PracticianName.data = u.PracticianName
        form.PracticianDepartment.data = u.PracticianDepartment
        form.course_work.data = u.course_work
        form.practice_work.data = u.practice_work
        form.laboratory_work.data = u.laboratory_work
    return render_template('form2_edit.html', numForm = numForm, group = group, sub = sub, form=form)


@app.route('/form12_promo/<username>/<numForm>', methods=['GET', 'POST'])
@login_required
def form12_promo(username, numForm):
    items1_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 1).count()
    if items1_1 != 0:
        items1_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 1).all()
    else:
        items1_1=0

    items1_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 2).count()
    if items1_2 != 0:
        items1_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 2).all()
    else:
        items1_2=0

    items1_3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 3).count()
    if items1_3 != 0:
        items1_3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 3).all()
    else:
        items1_3=0

    items1_4=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 4).count()
    if items1_4 != 0:
        items1_4=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1, Form_one.Course == 4).all()
    else:
        items1_4=0

    items2_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 1).count()
    if items2_1 != 0:
        items2_1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 1).all()
    else:
        items2_1=0

    items2_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 2).count()
    if items2_2 != 0:
        items2_2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2, Form_one.Course == 2).all()
    else:
        items2_2=0

    items3=Form_two.query.filter(Form_two.NumForm == numForm).all()

    items4=Form_all.query.filter(Form_all.id == numForm).first()

    koll = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).count() #Узнаем количество групп в заявке
    groups = Form_one.query.filter(Form_one.NumForm == numForm).all() #Узнаем номера групп
    G = []

    for i in groups:
        G.append(i.Group_id)

    all_g_ok = [0] * int(koll)
    k = 0
    for i in range(int(koll)):
        items=Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == G[i]).count()
        if items != 0:
            all_g_ok[i] = G[i]
            k = k + 1
        else:
             break
    items=Form_two

    items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
    items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()
    return render_template('form12_promo.html',
                            numForm = numForm,
                            items1 = items1, items2 = items2,
                            items2_1 = items2_1, items2_2 = items2_2,
                            items1_1 = items1_1, items1_2 = items1_2,
                            items1_3 = items1_3, items1_4 = items1_4,
                            items3 = items3, items = items,
                            FacultyU = items4.Faculty,
                            DepartmentU = items4.Department,
                            Year = items4.Year, koll = koll, G = G)
