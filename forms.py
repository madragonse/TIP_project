from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email

class RegistrationForm(FlaskForm):
    username = StringField('Nazwa', 
        validators=[DataRequired(), Length(min=3, max=27)])
    email = StringField('E-mail', 
        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź Hasło', 
        validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Zarejestruj')

class LoginForm(FlaskForm):
    username = StringField('E-mail', 
        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    
    submit = SubmitField('Zaloguj')