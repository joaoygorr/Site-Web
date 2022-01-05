from flask import render_template, redirect, request, url_for, flash
from site_web import app, database, bcrypt
from site_web.forms import FormSignIn, FormSignUp, FormEditProfile, FormCreatePost 
from site_web.models import Post, User
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template("home.html", posts=posts)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/user")
@login_required
def user():
    list_user = User.query.all()
    return render_template("user.html", list_user=list_user)

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
        # login depois de cadastrar
        user = User.query.filter_by(email=form_SignIn.email.data).first()
        login_user(user, remember=form_SignIn.remember_me.data) 
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

@app.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_post():
    form = FormCreatePost()
    if form.validate_on_submit(): 
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash("Post Successfully Created", "alert-success")
        return redirect(url_for("home"))
    return render_template("create_post.html", form=form)

def save_image(img): 
    cod = secrets.token_hex(8)
    name, extension = os.path.splitext(img.filename)
    name_archive = name + cod + extension
    full_path = os.path.join(app.root_path, 'static/media', name_archive)
    size = (400, 400)
    img_reduced = Image.open(img)
    img_reduced.thumbnail(size)
    img_reduced.save(full_path)
    return name_archive
    
def update_courses(form): 
    list_courses = []
    for field in form: 
        if 'course_' in field.name: 
            if field.data:
                list_courses.append(field.label.text)
    return ';'.join(list_courses)
            
@app.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile(): 
    form = FormEditProfile()
    if form.validate_on_submit(): 
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.profile_picture.data: 
            name_image = save_image(form.profile_picture.data)     
            current_user.profile_picture = name_image
        current_user.courses = update_courses(form)
        database.session.commit()
        flash("Profile Successfully Updated", "alert-success")
        return redirect(url_for('profile'))
    elif request.method == 'GET': # Mostra as informações já no campo 
        form.email.data = current_user.email 
        form.username.data = current_user.username
        # Retornando os campos já marcados (Courses)
        for field in form: 
            if 'course_' in field.name: 
                if field.label.text in current_user.courses: 
                    field.data = True
        
    profile_picture = url_for('static', filename=f'media/{current_user.profile_picture}')
    return render_template("edit_profile.html", profile_picture=profile_picture, form=form)

@app.route("/post/<post_id>")
def display_post(post_id): 
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)
    