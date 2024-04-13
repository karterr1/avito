from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class AdvertForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    phone_number = StringField('Номер телефона', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    description = PasswordField('Описание', validators=[DataRequired()])
    submit = SubmitField('Выложить')
