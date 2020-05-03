from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
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
    Faculty_id = SelectField('Факультет', coerce=int, validators=[DataRequired()])
    Department_id = SelectField('Кафедра', coerce=int, validators=[DataRequired()])
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
    submit = SubmitField('Начать заполнение формы')

class F_Two(FlaskForm):
    Degree_id = SelectField('Классификация', choices=[('1', 'Бакалавриат'),('2', 'Магистратура')])
    Course = StringField('Номер курса', validators=[DataRequired()])
    Direction_id = StringField('Код направление', validators=[DataRequired()])
    Direction_name = StringField('Название направление', validators=[DataRequired()])
    Profile_id = StringField('Код профиля',validators=[DataRequired()])
    Profile_name = StringField('Название профиля',validators=[DataRequired()])
    Group_id = StringField('Номер группы', validators=[DataRequired()])
    NumStudents = StringField('Число учащихся', validators=[DataRequired()])

    AddGroup = SubmitField('Добавить данные')
    SetUpForm = SubmitField('Отправить форму 1')

class F_Three(FlaskForm):
    NextForm = SubmitField('Перейти к форме 2')

class F_Four(FlaskForm):
    Degree_id = SelectField('Классификация', choices=[('1', 'Бакалавриат'),('2', 'Магистратура')])
    Course = StringField('Номер курса', validators=[DataRequired()])
    Direction_id = StringField('Код направление', validators=[DataRequired()])
    Direction_name = StringField('Название направление', validators=[DataRequired()])
    Profile_id = StringField('Код профиля',validators=[DataRequired()])
    Profile_name = StringField('Название профиля',validators=[DataRequired()])
    Group_id = StringField('Номер группы', validators=[DataRequired()])
    NumStudents = StringField('Число учащихся', validators=[DataRequired()])

    Save = SubmitField('Сохранить изменения')
