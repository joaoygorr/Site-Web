from flask import render_template, redirect, request, url_for, flash
from site_web import app, database, bcrypt
from site_web.forms import FormSignIn, FormSignUp, FormEditProfile
from site_web.models import User
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/user")
@login_required
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
            flash(f"Login Successfully In Email: {form_SignIn.email.data}", "alert-success")
            # Redirecionando 
            par_next = request.args.get("next")
            if par_next: 
                return redirect(par_next)
            else: 
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
        flash(f"Account Successfully Created For Email: {form_SignUp.email.data}", "alert-success")
        # Redirecionando
        return redirect(url_for("home"))
    
    return render_template("login.html", form_SignIn=form_SignIn, form_SignUp=form_SignUp)
    
@app.route("/exit")
@login_required
def exit():
    logout_user()
    flash(f"Successfully Logged Out", "alert-success")
    return redirect(url_for("home"))

    
@app.route("/profile")
@login_required
def profile():
    profile_picture = url_for('static', filename=f'media/{current_user.profile_picture}')
    return render_template("profile.html", profile_picture=profile_picture)

@app.route("/post/create")
@login_required
def create_post():
    return render_template("create_post.html")

@app.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile(): 
    form = FormEditProfile()
    if form.validate_on_submit(): 
        current_user.email = form.email.data
        current_user.username = form.username.data
        database.session.commit()
        flash(f"Profile Successfully Updated", "alert-success")
        return redirect(url_for('profile'))
    elif request.method == 'GET': # Mostra as informações já no campo 
        form.email.data = current_user.email 
        form.username.data = current_user.username
        
    profile_picture = url_for('static', filename=f'media/{current_user.profile_picture}')
    return render_template("edit_profile.html", profile_picture=profile_picture, form=form)