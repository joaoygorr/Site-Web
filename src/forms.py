from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class FormSign_up(FlaskForm): 
    username = StringField('username', validators=[DataRequired(), Length(6, 20)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    confirm = PasswordField("Password Confirmation", validators=[DataRequired(), EqualTo('password')])
    button_submit = SubmitField("Create Account")
    

class FormSign_in(FlaskForm): 
    email = SubmitField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    button_submit = SubmitField("Sign_In")
    