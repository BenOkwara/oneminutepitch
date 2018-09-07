from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))


    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return f'User {self.name}'


class Pitch:

    all_pitches = []

    def __init__(self,title,pitch):
        # self.movie_id = movie_id
        self.title = title
        # self.imageurl = imageurl
        self.pitch = pitch


    def save_pitch(self):
        Pitch.all_pitches.append(self)


    @classmethod
    def clear_pitch(cls):
        Pitch.all_pitches.clear()



