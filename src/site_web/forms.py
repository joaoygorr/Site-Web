from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from site_web.models import User
from flask_login import current_user

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
        
class FormEditProfile(FlaskForm): 
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    profile_picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    course_python = BooleanField("Python")
    course_nodejs = BooleanField("NodeJs")
    course_js = BooleanField("JavaScript")
    course_ts = BooleanField("TypeScript")
    course_reactjs = BooleanField("ReactJs")
    course_banco = BooleanField("Banco de Dados")
    button_EditProfile = SubmitField("Edit Profile")
    
    # Verificando se existe email igual no banco
    def validate_email(self, email): 
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user: 
                raise ValidationError("There Is Already A User With This Email")
        