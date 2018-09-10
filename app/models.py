from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    # Passes in a user id to this function and the function queries
    #  the database and gets a user's id as a response

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    pitches = db.relationship('Pitch', backref='user', lazy="dynamic")
    comments = db.relationship("Comment", backref="user", lazy="dynamic")
    votecounter = db.relationship("Countvotes", backref="user", lazy="dynamic")

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

class Pitch(db.Model):

    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(300), index=True)
    content = db.Column(db.String(300), index=True)
    category_id = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Comment', backref='pitch', lazy="dynamic")
    votecounter = db.relationship("Countvotes", backref="pitch", lazy="dynamic")
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def save_pitch(self, pitch):
        ''' Save the pitches '''
        db.session.add(pitch)
        db.session.commit()

    # display pitches
    @classmethod
    def get_pitches(id):
        pitches = Pitch.query.filter_by(category_id = id).all()
        return pitches

    def __repr__(self):
        return f"Pitch('{self.id}', '{self.time}')"

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_comment = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches = db.Column(db.Integer, db.ForeignKey('pitches.id'))
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def save_comment(self):
        ''' Save the comments '''
        db.session.add(self)
        db.session.commit()


    # display comments

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments

class Countvotes(db.Model):
    __tablename__ = 'countvotes'

    id = db.Column(db. Integer, primary_key=True)
    votecounter = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_votecounter(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votecounter(cls,user_id,pitches):
        votecounter = Countvotes.query.filter_by(user_id=user_id, pitches=pitches).all()
        return votecounter