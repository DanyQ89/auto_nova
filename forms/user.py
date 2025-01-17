from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class RegisterUser(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Номер телефона', validators=[DataRequired()])
    address = StringField('Адрес доставки', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class LoginUser(FlaskForm):
    phone = StringField('Номер', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Сохранить')



