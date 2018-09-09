from flask import render_template, request, redirect,url_for, abort, flash
from . import main
from .forms import PitchForm, UpdateProfile, CategoryForm, CommentForm
from ..models import Pitch, User, Category, Comment
from flask_login import login_required, current_user
from .. import db, photos
import markdown2

# INDEX PAGE
@main.route('/')
def index():
    """ View root page function that returns index page """

    category = Category.get_categories()

    title = 'WELCOME TO ONE MINUTE PITCH'
    return render_template('index.html', title = title, category = category)


# VIEWING EACH SPECIFIC PROFILE
@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

# UPDATING PROFILE

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

# UPDATING PICTURE
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

#display categories

@main.route('/category/<id>')
def category(id):
    '''
    view category function that returns the pitches of that category
    '''
    category = Category.query.get(id)

    if category is None:
        abort(404)

    title = f'{category.name} pitches'
    pitch = Pitch.get_pitches(category.id)

    return render_template('category.html', title = title, category = category, pitch = pitch)

# ADDING A NEW PITCH
@main.route('/pitch/new', methods=['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = Pitch(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(pitch)
        db.session.commit()
        flash('Your pitch has been created!', 'success')
        return redirect(url_for('main.new_pitch'))
    return render_template('newpitch.html', title='New Post', pitch_form=form, legend='New Post')



# ADDING A NEW PITCH IN A NEW CATEGORY WITH ITS OWN ID OF THE INTEGER FORM
#
# @main.route('/category/pitch/new/<int:id>', methods = ["GET", "POST"])
# @login_required
# def new_pitch(id):
#     '''
#     view category that returns a form to create a pitch
#     '''
#     form = PitchForm()
#     category = Category.query.filter_by(id = id).first()
#     if form.validate_on_submit():
#         title = form.title.data
#         post = form.post.data
#
#         # pitch instance
#         new_pitch = Pitch(category_id = category.id, title = title, post = post, user = current_user)
#
#         # save pitch
#         new_pitch.save_pitch()
#         return redirect(url_for('.category', id = category.id))
#     title = f'{category.name} pitches'
#     return render_template('newpitch.html', title = title, pitch_form = form, category = category)


# ADDING A NEW COMMENT TO A PITCH
@main.route('/pitch/comment/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
    '''
    view category that returns a form to create a new comment
    '''
    form = CommentForm()
    pitch = Pitch.query.filter_by(id = id).first()


    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data

        # comment instance
        new_comment = Comment(pitch_id = pitch.id, post_comment = comment, title=title, user = current_user)

        # save comment
        new_comment.save_comment()
        return redirect(url_for('.pitches', id = pitch.id ))

    title = f'{pitch.title} comment'
    return render_template('newcomment.html', title = title, comment_form = form, pitch = pitch, )

# TESTING HERE

@main.route('/add/category', methods=['GET','POST'])
@login_required
def new_category():
    '''
    View new group route function that returns a page with a form to create a category
    '''
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        new_category = Category(name=name)
        new_category.save_category()

        return redirect(url_for('.index'))

    title = 'New category'
    return render_template('newcategory.html', category_form = form,title=title)


@main.route('/comment/<int:id>')
def single_comment(id):
    comment=Comment.query.get(id)
    if comment is None:
        abort(404)
    format_comment = markdown2.markdown(comment.post_comment,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('comments.html',comment= comment,format_comment=format_comment)
