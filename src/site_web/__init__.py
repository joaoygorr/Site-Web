from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
  
app.config['SECRET_KEY'] = '8a8a95c229ba363bbfd4b6d538e65241'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web.db'

database = SQLAlchemy(app)
