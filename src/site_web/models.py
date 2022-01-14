from datetime import datetime
from site_web import database, login_manager
from flask_login import UserMixin

# Login
@login_manager.user_loader 
def load_user(id_user): 
    return User.query.get(int(id_user))

class User(database.Model, UserMixin): 
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    profile_picture = database.Column(database.String, default='default.jpg')
    courses = database.Column(database.String, nullable=False, default='Not Informed')
    posts = database.relationship('Post', backref='author', lazy=True)
    
    def count_post(self): 
        return len(self.posts)
    
class Post(database.Model): 
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    body = database.Column(database.Text, nullable=False)
    dt_create = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_user = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)