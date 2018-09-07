from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required

class PitchForm(FlaskForm):

    title = StringField('Pitch title',validators=[Required()])
    category_id = SelectField('Pitch Category', choices=[('product', 'product'),
                                                      ('service', 'service'),
                                                      ('fundraising', 'fundraising'),
                                                      ('business', 'business')])
    pitch = TextAreaField('Post Of The Pitch', validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):

    title = StringField('Pitch title',validators=[Required()])
    pitch = TextAreaField('Post Of The Comment', validators=[Required()])
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):

    title = StringField('Pitch title',validators=[Required()])
    pitch = TextAreaField('Post Of The Comment', validators=[Required()])
    submit = SubmitField('Submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')