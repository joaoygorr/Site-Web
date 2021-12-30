from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from site_web.models import User

class FormSignIn(FlaskForm): 
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    remember_me = BooleanField("Remember-me")
    button_submitIn = SubmitField("Sign_In")
    
class FormSignUp(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(6, 20)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    confirm = PasswordField("Password Confirmation", validators=[DataRequired(), EqualTo('password')])
    button_submitUp = SubmitField("Create Account")
    
    # Verificando se existe email igual no banco
    def validate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()
        if user: 
            raise ValidationError("E-mail Already Registered.")