from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AdvertForm(FlaskForm):  # форма для добавления, изменения работы
    title = StringField('Название', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    submit = SubmitField('Выложить')
