from flask import Flask, render_template

app = Flask(__name__)

list_user = []

@app.route("/")
def hello_world():
    return render_template("base.html")


@app.route("/users")
def user():
    return render_template("user.html")
    
if __name__ == "__main__": 
    app.run(debug=True)