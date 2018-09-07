from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique=True, index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return f'User {self.name}'
#
#
# class Pitch:
#
#     all_pitches = []
#
#     def __init__(self,title,pitch):
#         # self.movie_id = movie_id
#         self.title = title
#         # self.imageurl = imageurl
#         self.pitch = pitch
#
#
#     def save_pitch(self):
#         Pitch.all_pitches.append(self)
#
#
#     @classmethod
#     def clear_pitch(cls):
#         Pitch.all_pitches.clear()
#
#
#
