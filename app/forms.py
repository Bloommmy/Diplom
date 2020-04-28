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
    access = SelectField('Уровень доступа', choices=[
        ('admin', 'admin'),
        ('user', 'user'),
    ], default='user', validators=[DataRequired()])

    submit = SubmitField('Добавить пользователя в базу')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Данный электронный адрес уже зарегестрирован в системе.')

'''class FillingStageOne(FlaskForm):
    Degree_id = SelectField('Квалификация', coerce=int, validators=[DataRequired()])'''
