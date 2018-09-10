from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField

class PitchForm(FlaskForm):

    title = StringField('Pitch title')
    category_id = SelectField('Pitch Category', choices=[('product', 'product'),
                                                      ('service', 'service'),
                                                      ('fundraising', 'fundraising'),
                                                      ('business', 'business')])
    content = TextAreaField('Post Of The Pitch')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):

    title = StringField('Comment Title')
    comment = TextAreaField('Post Of The Comment')
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):

    title = StringField('Pitch title')
    pitch = TextAreaField('Post Of The Comment')
    submit = SubmitField('Submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.')
    submit = SubmitField('Submit')