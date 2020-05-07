
@app.route('/fsix/<username>/<numForm>', methods=['GET', 'POST'])
@login_required
def fsix(username, numForm):
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

    return render_template('fsix.html',
                            numForm = numForm,
                            items2_1 = items2_1, items2_2 = items2_1,
                            items1_1 = items1_1, items1_2 = items1_2,
                            items1_3 = items1_3, items1_4 = items1_4,
                            items3 = items3,
                            FacultyU = items4.Faculty,
                            DepartmentU = items4.Department,
                            Year = items4.Year)

@app.route('/fsix_edit/<username>/<numForm>/<group>/<sub>', methods=['GET', 'POST'])
@login_required
def fsix_edit(username, numForm, group, sub):
    form = F_six_edit()
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
        return redirect(url_for('fsix', username = current_user.username, numForm = numForm))

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
    return render_template('fsix_edit.html', numForm = numForm, group = group, sub = sub, form=form)










    class F_two_edit(FlaskForm):
        FullSubject = StringField('Полное', validators=[DataRequired()])
        BriefSubject = StringField('Краткое', validators=[DataRequired()])

        LecturerName = StringField('ФИО', validators=[DataRequired()])
        LecturerDepartment = StringField('Кафедра', validators=[DataRequired()])

        PracticianName = StringField('ФИО', validators=[DataRequired()])
        PracticianDepartment = StringField('Кафедра', validators=[DataRequired()])

        course_work = SelectField('Курсовая', choices=[('1', 'Да'),('2', 'Нет')])
        practice_work = SelectField('Практика', choices=[('1', 'Да'),('2', 'Нет')])
        laboratory_work = SelectField('Лабораторные',  choices=[('1', 'Да'),('2', 'Нет')])

        Save = SubmitField('Сохранить')




<td><a href="{{ url_for('form2_edit', username=current_user.username, numForm=numForm, group=item.Group_id, sub=item.id) }}">Изменить</a></td>

<td><a href="{{ url_for('form2_edit', username=current_user.username, numForm=numForm, group=item.Group_id, sub=item.id) }}">Изменить</a></td>
