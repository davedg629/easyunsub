from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = TextField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField()
