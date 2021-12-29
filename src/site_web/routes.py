from flask import render_template, redirect, request, url_for, flash
from site_web import app
from site_web.forms import FormSignIn, FormSignUp

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
        # Mensagem
        flash(f"login successfully in email: {form_SignIn.email.data}", "alert-success")
        # Redirecionando 
        return redirect(url_for("home"))

    if form_SignUp.validate_on_submit() and 'button_submitUp' in request.form:  # Conta criada
        # Mensagem
        flash(f"account successfully created for email: {form_SignUp.email.data}", "alert-success")
        # Redirecionando
        return redirect(url_for("home"))
    
    return render_template("login.html", form_SignIn=form_SignIn, form_SignUp=form_SignUp)
    