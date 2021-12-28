from flask import Flask, render_template, url_for
app = Flask(__name__)

list_user = []

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/login")
def login(): 
    return render_template("login.html")
    
if __name__ == "__main__": 
    app.run(debug=True)