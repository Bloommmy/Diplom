# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, jsonify, request
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
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.email import send_new_user
from app.forms import ResetPasswordForm
from app.forms import User_Search

import json

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

        flash('Пользователь успешно добавлен в базу')
        return render_template('RegistrationTotal.html', username=username, password=password, email=form.email.data, title='Итог регистрации')

    return render_template('register.html', title='Register', form=form)

@app.route('/send_login_pass/<login>/<parol>/<email>', methods=['GET', 'POST'])
@login_required
def send_login_pass(login, parol, email):
    FullName = User.query.filter(User.email == email, User.username == login).first().FullName
    s = send_new_user(FullName=FullName, email=email, username=login, parol=parol)
    if s == 1:
        flash('Письмо успешно отправленно на почту {}'.format(email))
        return render_template('RegistrationTotal.html', username=login, password=parol, email=email, title='Итог регистрации')
    else:
        flash('Что то пошло не так')
        return render_template('RegistrationTotal.html', username=login, password=parol, email=email, title='Итог регистрации')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        u = User.query.filter(User.username == current_user.username).first()
        u.FullName = form.FullName.data
        u.Phone = form.Phone.data
        db.session.commit()
        flash('Изменения успешно сохранены')
        return redirect(url_for('PersonalArea', username=current_user.username))
    elif request.method == 'GET':
        u = User.query.filter(User.username == current_user.username).first()
        form.username.data = current_user.username
        form.FullName.data = u.FullName
        form.Phone.data = u.Phone

    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/reset_password_request/<username>', methods=['GET', 'POST'])
def reset_password_request(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Проверьте свою электронную почту для получения инструкций по сбросу пароля')
        return redirect(url_for('PersonalArea', username=current_user.username))
    return render_template('reset_password_request.html', title='Сброс пароля', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Пароль успешно изменен')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/form0/<username>/<i>', methods=['GET', 'POST'])
@login_required
def form0(username, i):
    def check(f1):
        if f1 != 0:
            f1 = Form_one.query.filter(Form_one.NumForm == numForm).all()

            items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
            items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()
            items3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 3).count()

            items = Form_one
            b = [1,2,3,4]
            m = [1,2]
            c = [1,2,3,4,5]

            f2 = Form_two.query.filter(Form_two.NumForm == numForm).count()
            if f2 != 0:
                f2 = Form_two.query.filter(Form_two.NumForm == numForm).all()
            else:
                f2 = 0
        else:
            f1 = 0
            f2 = 0
            items = 0
            items1 = 0
            items2 = 0
            items3 = 0
            b = 0
            c = 0
            m = 0

        return (f1, f2, items, items1, items2, items3, b, m, c)

    user = User.query.filter_by(username=username).first_or_404()

    #Проверка на наличие незаконченных заявок
    f0 = Form_all.query.filter(Form_all.user_id == user.id, Form_all.Status == None).count()

    if f0 != 0: #Если есть незаконченные заявки
        f0 = Form_all.query.filter(Form_all.user_id == user.id, Form_all.Status == None).first()
        numForm = f0.id  #Выясняем номер заявки
        f1 = Form_one.query.filter(Form_one.NumForm == numForm).count()
        f1, f2, items, items1, items2, items3, b, m, c = check(f1)
        if f2 != 0:
            koll = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).count() #Узнаем количество групп в заявке
            groups = Form_one.query.filter(Form_one.NumForm == numForm).all() #Узнаем номера групп
            G = []

            for u in groups:
                G.append(u.Group_id)
            k = 0
            g_no_ok = []
            for u in range(koll):
                it=Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == G[u]).count()
                if it == 0:
                    g_no_ok.append(G[u])
                    k = k + 1
                else:
                     continue
        else:
            G = 0
            koll = 0
            k = 0
            items_2 = 0
            g_no_ok = 0


        items_2=Form_two
        return render_template('form0.html',
                                numForm = numForm,
                                Faculty = 0, Department = 0, Year = 0, user = user,
                                k = k, g_no_ok = g_no_ok,
                                f0 = f0, f1 = f1, f2 = f2, items = items,
                                items1 = items1, items2 = items2, items3 = items3,
                                b = b, m = m, c = c,
                                koll = koll, G = G, items_2 = items_2)



    elif f0 == 0: #если нет незаконченных заявок
        Faculty = user.Faculty
        Department = user.Department
        Year = "весна 2020"

        f=Form_all.query.order_by(Form_all.timestamp.desc()).count() #задаем номер заявки
        if f == 0:
            numForm = 1
        else:
            f=Form_all.query.order_by(Form_all.timestamp.desc()).first().id
            numForm = int(f) + 1

        #Заносим в базу форму0
        form0 = Form_all(user_id = user.id,Faculty = Faculty, Department = Department, Year = Year)
        db.session.add(form0)
        db.session.commit()
        numForm = int(Form_all.query.order_by(Form_all.timestamp.desc()).first().id)

        return render_template('form0.html', f0 = 0, numForm = numForm,
                                Faculty = Faculty, Department = Department,
                                Year = Year, user = user, i = i)

@app.route('/form_delet/<username>/<numForm>/<i>/<g>/<sub>')
@login_required
def form_delet(username, numForm,i, g, sub):
    user = User.query.filter_by(username=username).first_or_404()
    if i == '1':
        f = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == g).first()
        db.session.delete(f)
        db.session.commit()
        flash('Группа {} успешно удалена'.format(g))
        return redirect(url_for('form1_promo', username = current_user.username, numForm = numForm, i = 1))

    elif i == '2':
        f = Form_all.query.get(numForm)
        db.session.delete(f)
        db.session.commit()
        flash('Заявка {} успешно удалена'.format(numForm))
        return redirect(url_for('index'))

    elif i == '11':
        f = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == g).first()
        db.session.delete(f)
        db.session.commit()
        flash('Группа {} успешно удалена'.format(g))
        return redirect(url_for('form12_promo', username = current_user.username, numForm = numForm, i = 1))
    elif i == '12':
        f = Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == g, Form_two.id == sub).first()
        db.session.delete(f)
        db.session.commit()
        flash('Дисциплина успешно удалена')
        return redirect(url_for('form12_promo', username = current_user.username, numForm = numForm, i = 1))
    elif i == '21':
        f = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == g).first()
        db.session.delete(f)
        db.session.commit()
        flash('Группа {} успешно удалена'.format(g))
        return redirect(url_for('form0_edit', username = current_user.username, numForm = numForm))
    elif i == '22':
        f = Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == g, Form_two.id == sub).first()
        db.session.delete(f)
        db.session.commit()
        flash('Дисциплина успешно удалена')
        return redirect(url_for('form0_edit', username = current_user.username, numForm = numForm))
    elif i == '3':
        f = Form_all.query.get(numForm)
        db.session.delete(f)
        db.session.commit()
        flash('Заявка {} успешно удалена'.format(numForm))
        return redirect(url_for('all_form_view', username = current_user.username))
    elif i == '44':
        f = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == g).first()
        db.session.delete(f)
        db.session.commit()
        flash('Группа {} успешно удалена'.format(g))
        return redirect(url_for('all_form_view_g', username = current_user.username, numForm = numForm))
    elif i == '55':
        f = Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == g, Form_two.id == sub).first()
        db.session.delete(f)
        db.session.commit()
        flash('Дисциплина успешно удалена')
        return redirect(url_for('all_form_view_g', username = current_user.username, numForm = numForm))




@app.route('/form_clean/<username>/<numForm>/<i>')
@login_required
def form_clean(username, numForm, i):
    if i == '21':
        form1 = Form_one.query.filter(Form_one.NumForm == numForm).all()
        for f in form1:
            db.session.delete(f)
        db.session.commit()
        flash('Форма 1 и 2 успешно отчищена')
        return redirect(url_for('form0_edit', username = current_user.username, numForm = numForm))
    elif i == '22':
        form2 = Form_two.query.filter(Form_two.NumForm == numForm).all()
        for f in form2:
            db.session.delete(f)
        db.session.commit()
        flash('Форма 2 успешно отчищена')
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
            items3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 3).count()

            items = Form_one
            b = [1,2,3,4]
            m = [1,2]
            c = [1,2,3,4,5]

            f2 = Form_two.query.filter(Form_two.NumForm == numForm).count()
            if f2 != 0:
                f2 = Form_two.query.filter(Form_two.NumForm == numForm).all()
            else:
                f2 = 0
        else:
            f1 = 0
            f2 = 0
            items = 0
            items1 = 0
            items2 = 0
            items3 = 0
            b = 0
            c = 0
            m = 0

        return (f1, f2, items, items1, items2, items3, b, m, c)

    f0 = Form_all.query.filter(Form_all.user_id == user.id, Form_all.id == numForm).first()
    f1 = Form_one.query.filter(Form_one.NumForm == numForm).count()
    f1, f2, items, items1, items2, items3, b, m, c = check(f1)
    if f2 != 0:
        koll = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).count() #Узнаем количество групп в заявке
        groups = Form_one.query.filter(Form_one.NumForm == numForm).all() #Узнаем номера групп
        G = []

        for i in groups:
            G.append(i.Group_id) #записываем группы в массив

        all_g_ok = [0] * int(koll) #создаем нулевой массив равный количеству групп
        k = 0
        g_no_ok = []
        for u in range(koll):
            it=Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == G[u]).count()
            if it == 0:
                g_no_ok.append(G[u])
                k = k + 1
            else:
                 continue
        items_2=Form_two

    else:
        G = 0
        koll = 0
        k = 0
        items_2 = 0
        g_no_ok = 0

    return render_template('form0_edit.html',
                            numForm = numForm, g_no_ok = g_no_ok, k = k,
                            user = user, G = G, koll = koll,
                            items = items, items_2 = items_2,
                            f0 = f0, f1 = f1, f2 = f2,
                            items1 = items1, items2 = items2, tems3 = items3,
                            b = b, m = m, c = c)

@app.route('/form1/<username>/<numForm>/<g>/<i>', methods=['GET', 'POST'])
@login_required
def form1(username, numForm, g, i):
    user = User.query.filter_by(username=username).first_or_404()
    numForm = int(numForm)
    g = int(g)
    form = F_One()

    def check_the_entered_data(g, i): #проверка корректности введенных данных
         check_group = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == form.Group_id.data).count() #проверяем есть ли в базе данная группа
         check_degree = form.Degree_id.data
         check_course = form.Course.data

         if check_group == 1:
             flash('Группа {} уже есть в заявку, пожалуйста, введите другой номер группы'.format(form.Group_id.data))
             g = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).first().Group_id
             return redirect(url_for('form1', username = current_user.username, numForm = numForm, g = g, i = i))
         elif check_degree == 1 and check_course == 5:
             flash('Неправильно указан номер курса либо классификация')
             return redirect(url_for('form1', username = current_user.username, numForm = numForm, g = g, i = i))
         elif check_degree == 2 and (check_course == 3 or check_course == 4 or check_course == 5):
             flash('Неправильно указан номер курса либо классификация')
             return redirect(url_for('form1', username = current_user.username, numForm = numForm, g = g, i = i))
         else:
             return 1

    def add_form1(numForm, g, i):

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
        g = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).first().Group_id
        return g


    if form.validate_on_submit():
        status = check_the_entered_data(g = g, i = i)
        if status == 1:
            g = add_form1(numForm = numForm, g = g, i = i)
            flash('Данные о группе {} успешно добавлены'.format(g))
            return redirect(url_for('form1', username = current_user.username, numForm = numForm, g = g, i = i))

    elif request.method == 'GET':
        u = Form_one.query.filter(Form_one.NumForm == numForm, ).order_by(Form_one.timestamp.desc()).first()
        if u != None:
            g = u.Group_id
            form.Group_id.data = u.Group_id
            form.Degree_id.data = u.Degree_id
            form.Direction_id.data = u.Direction_id
            form.Direction_name.data = u.Direction_name
            form.Profile_id.data = u.Profile_id
            form.Profile_name.data = u.Profile_name
            form.Course.data = u.Course
            form.NumStudents.data = u.NumStudents


    if g == 0 and (i == '1' or i == '23'):
        items1=0
        items2=0
        items3=0
        items = 0
        b = 0
        m = 0
        c = 0

    elif g != 0 and i == '1':
        items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
        items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()
        items3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 3).count()
        items = Form_one
        b = [1,2,3,4]
        m = [1,2]
        c = [1,2,3,4,5]
    elif i == '11' or i == '21' or i == '22' or i == '23' or i == '44':
        items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
        items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()
        items3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 3).count()
        items = Form_one
        b = [1,2,3,4]
        m = [1,2]
        c = [1,2,3,4,5]

    return render_template('form1.html',
                            numForm = numForm,
                            items = items, b = b, c = c, m = m,
                            items1 = items1, items2 = items2, items3 = items3,
                            g = g,  i = i, form = form)

@app.route('/form1_promo/<username>/<numForm>/<i>', methods=['GET', 'POST'])
@login_required
def form1_promo(username, numForm, i):
    items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
    items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()
    items3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 3).count()
    items = Form_one
    b = [1,2,3,4]
    m = [1,2]
    c = [1,2,3,4,5]


    return render_template('form1_promo.html',
                            numForm = numForm, items = items, b = b, m = m, c = c,
                            items1 = items1, items2 = items2, items3 = items3, i = i)

@app.route('/form1_edit/<username>/<numForm>/<group>/<i>', methods=['GET', 'POST'])
@login_required
def form1_edit(username, numForm, group, i):
    i = i
    form = F_One_edit()
    if form.validate_on_submit():
        h = Form_all.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == form.Group_id.data).count()
        if h == 1 and int(form.Group_id.data) != int(group):
            flash('Группа с номером {} уже внесены в заявку, пожалуйста, введите другой номер группы'.format(form.Group_id.data))
            return redirect(url_for('form1_edit', username = current_user.username, numForm = numForm, group = group, i = i))
        else:
            deg = str(form.Degree_id.data)
            cou = str(form.Course.data)
            if deg == '2' and (cou == '3' or cou == '4' or cou == '5'):
                flash('Неправильно указан номер курса либо классификация')
                return redirect(url_for('form1_edit', username = current_user.username, numForm = numForm, group = group, i = i))
            elif deg == '1' and cou == '5':
                flash('Неправильно указан номер курса либо классификация')
                return redirect(url_for('form1_edit', username = current_user.username, numForm = numForm, group = group, i = i))
            else:
                f = Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == group).count()
                if f != 0:
                    f = Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == group).all()
                    for u in f:
                        u.Group_id = form.Group_id.data
                        db.session.commit()
                    else:
                        f = 0

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
        flash('Изменения в группе {} успешно сохранены'.format(form.Group_id.data))
        if i == '1':
            return redirect(url_for('form1_promo', username = current_user.username, numForm = numForm, i = 1))
        elif i == '11':
            return redirect(url_for('form12_promo', username = current_user.username, numForm = numForm, i = 1))
        elif i == '2':
            return redirect(url_for('form0_edit', username = current_user.username, numForm = numForm))
        elif i == '44':
            return redirect(url_for('all_form_view_g', username = current_user.username, numForm = numForm))

    elif request.method == 'GET':
        u = Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Group_id == group).first()
        form.Degree_id.data = u.Degree_id
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
    g = int(g)
    p = int(p)
    for u in groups:
        G.append(u.Group_id)
    if g == 0:
        g = G[int(p)]
    else:
        g = g
    form = F_Two()


    def addForm_two(g):
        g = str(g)

        f=Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == g).order_by(Form_two.timestamp.desc()).count()
        if f == 0:
            sub = 1
        else:
            f=Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == g).order_by(Form_two.timestamp.desc()).first().id
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



    f=Form_two.query.filter(Form_two.NumForm == numForm).order_by(Form_two.timestamp.desc()).count()
    all_g_ok = [0] * int(koll)
    k = 0
    for l in range(int(koll)):
        items=Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == G[l]).count()
        if items != 0:
            all_g_ok[l] = G[l]
            k = k + 1
        else:
             continue

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
        if i == '2':
            return redirect(url_for('form0_edit', username = current_user.username, numForm = numForm))
        elif i == '1':
            return redirect(url_for('form12_promo', username = current_user.username, numForm = numForm, i = 1))
        elif i == '44':
            return redirect(url_for('all_form_view_g', username = current_user.username, numForm = numForm))

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
    return render_template('form2_edit.html', numForm = numForm, group = group, sub = u.FullSubject, form=form, i = i)

@app.route('/form12_promo/<username>/<numForm>/<i>', methods=['GET', 'POST'])
@login_required
def form12_promo(username, numForm, i):
    user = User.query.filter_by(username=username).first_or_404()
    def check(f1):
        if f1 != 0:
            f1 = Form_one.query.filter(Form_one.NumForm == numForm).all()

            items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
            items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()
            items3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 3).count()

            items = Form_one
            b = [1,2,3,4]
            m = [1,2]
            c = [1,2,3,4,5]

            f2 = Form_two.query.filter(Form_two.NumForm == numForm).count()
            if f2 != 0:
                f2 = Form_two.query.filter(Form_two.NumForm == numForm).all()
            else:
                f2 = 0
        else:
            f1 = 0
            f2 = 0
            items = 0
            items1 = 0
            items2 = 0
            items3 = 0
            b = 0
            c = 0
            m = 0

        return (f1, f2, items, items1, items2, items3, b, m, c)

    f0 = Form_all.query.filter(Form_all.user_id == user.id, Form_all.id == numForm).first()
    f1 = Form_one.query.filter(Form_one.NumForm == numForm).count()
    f1, f2, items, items1, items2, items3, b, m, c = check(f1)
    if f2 != 0:
        koll = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).count() #Узнаем количество групп в заявке
        groups = Form_one.query.filter(Form_one.NumForm == numForm).all() #Узнаем номера групп
        G = []

        for i in groups:
            G.append(i.Group_id) #записываем группы в массив

        all_g_ok = [0] * int(koll) #создаем нулевой массив равный количеству групп
        k = 0
        g_no_ok = []
        for u in range(koll):
            it=Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == G[u]).count()
            if it == 0:
                g_no_ok.append(G[u])
                k = k + 1
            else:
                 continue
        items_2=Form_two

    else:
        G = 0
        koll = 0
        k = 0
        items_2 = 0
        g_no_ok = 0

    return render_template('form12_promo.html',
                            numForm = numForm, g_no_ok = g_no_ok, k = k, i = i, user = user, G = G, koll = koll,
                            items = items, items_2 = items_2,
                            f0 = f0, f1 = f1, f2 = f2,
                            items1 = items1, items2 = items2, tems3 = items3,
                            b = b, m = m, c = c)

@app.route('/send_request/<username>/<numForm>', methods=['GET', 'POST'])
@login_required
def send_request(username, numForm):
    form = Form_all.query.filter(Form_all.id == numForm).count()
    if form == 1:
        form = Form_all.query.filter(Form_all.id == numForm).first()
        form.Status = 'ok'
        db.session.commit()
        flash('Заявка успешно отправлена')
    else:
        flash('Данная заявка не найдена')
    return redirect(url_for('index'))



@app.route('/all_form_view_g/<username>/<numForm>', methods=['GET', 'POST'])
@login_required
def all_form_view_g(username, numForm):
    user = User.query.filter_by(username=username).first_or_404()


    def check(f1):
        if f1 != 0:
            f1 = Form_one.query.filter(Form_one.NumForm == numForm).all()

            items1=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 1).count()
            items2=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 2).count()
            items3=Form_one.query.filter(Form_one.NumForm == numForm, Form_one.Degree_id == 3).count()

            items = Form_one
            b = [1,2,3,4]
            m = [1,2]
            c = [1,2,3,4,5]

            f2 = Form_two.query.filter(Form_two.NumForm == numForm).count()
            if f2 != 0:
                f2 = Form_two.query.filter(Form_two.NumForm == numForm).all()
            else:
                f2 = 0
        else:
            f1 = 0
            f2 = 0
            items = 0
            items1 = 0
            items2 = 0
            items3 = 0
            b = 0
            c = 0
            m = 0

        return (f1, f2, items, items1, items2, items3, b, m, c)


    f0 = Form_all.query.filter(Form_all.id == numForm).first()
    f1 = Form_one.query.filter(Form_one.NumForm == numForm).count()
    f1, f2, items, items1, items2, items3, b, m, c = check(f1)
    if f2 != 0:
        koll = Form_one.query.filter(Form_one.NumForm == numForm).order_by(Form_one.timestamp.desc()).count() #Узнаем количество групп в заявке
        groups = Form_one.query.filter(Form_one.NumForm == numForm).all() #Узнаем номера групп
        G = []

        for n in groups:
            G.append(n.Group_id) #записываем группы в массив

        all_g_ok = [0] * int(koll) #создаем нулевой массив равный количеству групп
        k = 0
        g_no_ok = []
        for u in range(koll):
            it=Form_two.query.filter(Form_two.NumForm == numForm, Form_two.Group_id == G[u]).count()
            if it == 0:
                g_no_ok.append(G[u])
                k = k + 1
            else:
                 continue
        items_2=Form_two
    else:
        G = 0
        koll = 0
        k = 0
        items_2 = 0
        g_no_ok = 0
    return render_template('all_form_view_g.html',
                            numForm = numForm, g_no_ok = g_no_ok, k = k, user = user, G = G, koll = koll,
                            items = items, items_2 = items_2,
                            f0 = f0, f1 = f1, f2 = f2,
                            items1 = items1, items2 = items2, tems3 = items3,
                            b = b, m = m, c = c)

@app.route('/all_form_view/<username>', methods=['GET', 'POST'])
@login_required
def all_form_view(username):
    koll = Form_all.query.count() #выяснеем количество заявок
    if koll != 0:
        forms = Form_all.query.all()
        Z1 = []
        for f in forms: #получаем список заявок
            Z1.append(f.id)
        koll1 = Form_all.query.count()

        n2 = 0
        Z2 = []
        for f in forms: #получаем список различных годов в заявке
            if len(Z2) == 0:
                Z2.append(f.Year)
                n2 = n2 + 1
            elif Z2[n2 - 1] == f.Year:
                continue
            elif Z2[n2 - 1] != f.Yaer:
                Z2.append(f.Year)
                n2 = n2 + 1
        koll2 = len(Z2)

        Z3 = []
        n3 = 0
        for f in forms: #получаем список различных годов в заявке
            if len(Z3) == 0:
                Z3.append(f.user_id)
                n3 = n3 + 1
            elif Z3[n3 - 1] == f.user_id:
                continue
            elif Z3[n3 - 1] != f.user_id:
                Z3.append(f.user_id)
                n3 = n3 + 1
        koll3 = len(Z3)

        Z4 = []
        n4 = 0
        for f in forms: #получаем список различных годов в заявке
            if len(Z4) == 0:
                Z4.append(f.Department)
                n4 = n4 + 1
            elif Z4[n4 - 1] == f.Department:
                continue
            elif Z4[n4 - 1] != f.Department:
                Z4.append(f.Department)
                n4 = n4 + 1
        koll4 = len(Z4)

        Z5 = []
        n5 = 0
        for f in forms: #получаем список различных годов в заявке
            if len(Z5) == 0:
                Z5.append(f.Faculty)
                n5 = n5 + 1
            elif Z5[n5 - 1] == f.Faculty:
                continue
            elif Z5[n5 - 1] != f.Faculty:
                Z5.append(f.Faculty)
                n5 = n5 + 1
        koll5 = len(Z5)

        Z6 = []
        n6 = 0
        for f in forms: #получаем список различных годов в заявке
            if len(Z6) == 0:
                Z6.append(f.Status)
                n6 = n6 + 1
            elif Z6[n6 - 1] == f.Status:
                continue
            elif Z6[n6 - 1] != f.Status:
                Z6.append(f.Status)
                n6 = n6 + 1
        koll6 = len(Z6)

        all_forms = Form_all
        all_users = User
    else:
        koll1 = 0
        Z1 = 0
        koll2 = 0
        Z2 = 0
        koll3 = 0
        Z3 = 0
        koll4 = 0
        Z4 = 0
        koll5 = 0
        Z5 = 0
        koll6 = 0
        Z6 = 0
        all_forms = 0
        all_users = 0

    return render_template('all_form_view.html',
                            koll1 = koll1, Z1 = Z1,
                            koll2 = koll2, Z2 = Z2,
                            koll3 = koll3, Z3 = Z3,
                            koll4 = koll4, Z4 = Z4,
                            koll5 = koll5, Z5 = Z5,
                            koll6 = koll6, Z6 = Z6,
                            all_forms = all_forms, all_users = all_users)

@app.route('/all_form_user/<username>', methods=['GET', 'POST'])
@login_required
def all_form_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    users = User.query.all()
    group1=[]
    group2=[]
    group3=[]
    group4=[]
    group5=[]
    for u in users:
        name = u.FullName
        if name[0] == 'А' or name[0] == 'Б' or name[0] == 'В' or name[0] == 'Г' or name[0] == 'Д' or name[0] == 'Е' or name[0] == 'Ё':
            group1.append(u.id)
        elif name[0] == 'Ж' or name[0] == 'З' or name[0] == 'И' or name[0] == 'Й' or name[0] == 'К' or name[0] == 'Л' or name[0] == 'М':
            group2.append(u.id)
        elif name[0] == 'Н' or name[0] == 'О' or name[0] == 'П' or name[0] == 'Р' or name[0] == 'С' or name[0] == 'Т' or name[0] == 'У':
            group3.append(u.id)
        elif name[0] == 'Ф' or name[0] == 'Х' or name[0] == 'Ц' or name[0] == 'Ч' or name[0] == 'Ш' or name[0] == 'Щ':
            group4.append(u.id)
        elif name[0] == 'Ы' or name[0] == 'Ъ' or name[0] == 'Ь' or name[0] == 'Э' or name[0] == 'Ю' or name[0] == 'Я':
            group5.append(u.id)
    All_User = User
    res = 0
    form = User_Search()
    if form.validate_on_submit():
        if form.TypeSearch.data == 1:
            res = User.query.filter(User.FullName.like('%'+form.WhoSearch.data+'%'))
        elif form.TypeSearch.data == 2:
            res = User.query.filter(User.Department.like('%'+form.WhoSearch.data+'%'))
        elif form.TypeSearch.data == 3:
            res = User.query.filter(User.username.like('%'+form.WhoSearch.data+'%'))






    return render_template('all_form_user.html', form = form, All_User = All_User,
                            group1 = group1, group2 = group2, res = res,
                            group3 = group3, group4 = group4, group5 = group5,
                            koll1 = len(group1), koll2 = len(group2), koll3 = len(group3),
                            koll4 = len(group4), koll5 = len(group5))
