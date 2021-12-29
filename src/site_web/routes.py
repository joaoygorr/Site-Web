from flask import render_template, redirect, request, url_for, flash
from site_web import app, database, bcrypt
from site_web.forms import FormSignIn, FormSignUp
from site_web.models import User
from flask_login import login_user

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/login", methods=['GET', 'POST'])
def login(): 
    form_SignIn = FormSignIn()
    form_SignUp = FormSignUp()
    
    if form_SignIn.validate_on_submit() and 'button_submitIn' in request.form: # Login realizado
        # Verificando dados se existem para login 
        user = User.query.filter_by(email=form_SignIn.email.data).first()
        # ERROR ValueError: Invalid Salt
        if user and bcrypt.check_password_hash(user.password.encode('utf-8'), form_SignIn.password.data): 
            login_user(user, remember=form_SignIn.remember_me.data) 
            # Mensagem
            flash(f"Login Successfully In Email: {form_SignIn.email.data}", "alert")
            # Redirecionando 
            return redirect(url_for("home"))
        else: 
            flash(f"The Email Address Or Password You Entered Is Incorrect.", "alert-danger")

    if form_SignUp.validate_on_submit() and 'button_submitUp' in request.form:  # Conta criada
        # Criptografando senha 
        password_cript = bcrypt.generate_password_hash(form_SignUp.password.data).decode('utf-8')
        # Criando usuário
        user = User(username=form_SignUp.username.data, email=form_SignUp.email.data, password=password_cript)
        database.session.add(user)
        database.session.commit()
        # Mensagem
        flash(f"Account Successfully Created For Email: {form_SignUp.email.data}", "alert")
        # Redirecionando
        return redirect(url_for("home"))
    
    return render_template("login.html", form_SignIn=form_SignIn, form_SignUp=form_SignUp)
    