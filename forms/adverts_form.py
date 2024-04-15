from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class AdvertForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Выложить')
