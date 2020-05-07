from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить мне')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    FullName = StringField('ФИО', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    Phone = StringField('Контактный номер', validators=[DataRequired()])
    Faculty = StringField('Факультет', validators=[DataRequired()])
    Department = StringField('Кафедра', validators=[DataRequired()])
    access = SelectField('Уровень доступа', choices=[('admin', 'admin'),('user', 'user')], default='user', validators=[DataRequired()])

    submit = SubmitField('Добавить пользователя в базу')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Данный электронный адрес уже зарегестрирован в системе.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class F_One(FlaskForm):
    Degree_id = SelectField('Классификация', choices=[('1', 'Бакалавриат'),('2', 'Магистратура')])
    Course = IntegerField('Номер курса', validators=[DataRequired(), Optional()])
    Direction_id = IntegerField('Код направление', validators=[DataRequired()])
    Direction_name = StringField('Название направление', validators=[DataRequired()])
    Profile_id = IntegerField('Код профиля',validators=[DataRequired()])
    Profile_name = StringField('Название профиля',validators=[DataRequired()])
    Group_id = IntegerField('Номер группы', validators=[DataRequired()])
    NumStudents = IntegerField('Число учащихся', validators=[DataRequired()])

    AddGroup = SubmitField('Добавить данные')
    SetUpForm = SubmitField('Отправить форму 1')

    def validate_optional(self):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Данный электронный адрес уже зарегестрирован в системе.')

class F_One_edit(FlaskForm):
    Degree_id = SelectField('Классификация', choices=[('1', 'Бакалавриат'),('2', 'Магистратура')])
    Course = IntegerField('Номер курса', validators=[DataRequired()])
    Direction_id = IntegerField('Код направление', validators=[DataRequired()])
    Direction_name = StringField('Название направление', validators=[DataRequired()])
    Profile_id = IntegerField('Код профиля',validators=[DataRequired()])
    Profile_name = StringField('Название профиля',validators=[DataRequired()])
    Group_id = IntegerField('Номер группы', validators=[DataRequired()])
    NumStudents = IntegerField('Число учащихся', validators=[DataRequired()])

    Save = SubmitField('Сохранить изменения')

class F_Two(FlaskForm):
    FullSubject = StringField('Полное', validators=[DataRequired()])
    BriefSubject = StringField('Краткое', validators=[DataRequired()])

    LecturerName = StringField('ФИО', validators=[DataRequired()])
    LecturerDepartment = StringField('Кафедра', validators=[DataRequired()])

    PracticianName = StringField('ФИО', validators=[DataRequired()])
    PracticianDepartment = StringField('Кафедра', validators=[DataRequired()])

    course_work = SelectField('Курсовая', choices=[('1', 'Да'),('2', 'Нет')])
    practice_work = SelectField('Практика', choices=[('1', 'Да'),('2', 'Нет')])
    laboratory_work = SelectField('Лабораторные',  choices=[('1', 'Да'),('2', 'Нет')])

    AddSub = SubmitField('Добавить данные')

class F_Two_edit(FlaskForm):
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
