from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormSignIn, FormSignUp
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

list_user = []

app.config['SECRET_KEY'] = '8a8a95c229ba363bbfd4b6d538e65241'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web.db'

database = SQLAlchemy(app)

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
    
if __name__ == "__main__": 
    app.run(debug=True)