from datetime import datetime
from main import database
from datetime import datetime

class User(database.Model): 
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    profile_picture = database.Column(database.String, default='default.jpg')
    
class Post(database.Model): 
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    body = database.Column(database.Text, nullable=False)
    dt_create = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    
    