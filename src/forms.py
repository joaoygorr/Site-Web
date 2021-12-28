from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class FormSignIn(FlaskForm): 
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    remember_me = BooleanField("Remember-me")
    button_submit = SubmitField("Sign_In")
    
class FormSignUp(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(6, 20)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    confirm = PasswordField("Password Confirmation", validators=[DataRequired(), EqualTo('password')])
    button_submit = SubmitField("Create Account")
    
