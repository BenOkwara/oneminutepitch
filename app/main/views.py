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
    pitches = Pitch.query.all()

    title = 'WELCOME TO ONE MINUTE PITCH'
    return render_template('index.html', title = title, category = category, pitches=pitches)

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

# VIEW INDIVIDUAL PITCH

@main.route('/pitch/new/<int:id>')
def single_pitch(id):
    pitch = Pitch.query.get(id)
    return render_template('singlepitch.html',pitch = pitch)


@main.route('/allpitches')
def pitch_list():
    # Function that renders the business categorypitches and its content

    pitches = Pitch.query.all()

    return render_template('pitches.html', pitches=pitches)

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

# testing here

@main.route('/pitch/<int:pitch_id>/',methods=["GET","POST"])
def pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_pitch_comment = Comment(comment=comment,
                                    pitch_id=pitch_id,
                                    user_id=current_user.id)

        db.session.add(new_pitch_comment)
        db.session.commit()
    comments = Comment.query.all()
    return render_template('pitchlink.html', title=pitch.title, pitch=pitch, pitch_form=form, comments=comments)


@main.route('/pitch/<int:pitch_id>/update', methods=['GET','POST'])
@login_required
def update_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if pitch.author != current_user:
        abort(403)
    form = PitchForm()
    if form.validate_on_submit():
        pitch.title = form.title.data
        pitch.post = form.post.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.pitchlink', pitch_id=pitch.id))
    elif request.method == 'GET':
        form.title.data = pitch.title
        form.content.data = pitch.content
    return render_template('newpitch.html', title='Update Pitch', form=form, legend='Update Pitch')

@main.route('/pitch/<int:pitch_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    for comment in pitch.comments.all():
        db.session.delete(comment)
        db.session.commit()
    if pitch.author != current_user:
        abort(403)
    db.session.delete(pitch)
    db.session.commit()
    flash('Your pitch has been deleted!', 'success')
    return redirect(url_for('main.pitches'))


@main.route("/view/<id>", methods=["GET","POST"])
def view_pitch(id):
    pitch = Pitch.query.get(id)
    if request.args.get("vote"):
       pitch.likes = pitch.likes + 1
       pitch.save_pitch()
       return redirect("/view/{pitch_id}".format(pitch_id=id))
    return render_template('view_pitch.html',pitch = pitch,)




@main.route('/product')
def product():
    """
    Function that renders the product category pitches and its content
    """
    product_pitch = Pitch.query.filter_by(category='product').all()

    return render_template('product.html', product=product_pitch)


@main.route('/service')
def service():
    """
    Function that renders the service category pitches and its content
    """

    service_pitch = Pitch.query.filter_by(category='service').all()

    return render_template('service.html', service=service_pitch)


@main.route('/fundraising')
def fundraising():
    """
    Function that renders the fundraising category pitches and its content
    """

    fundraising_pitch = Pitch.query.filter_by(category='fundraising').all()

    return render_template('fundraising.html', fundraising=fundraising_pitch)


@main.route('/business')
def business():
    """
    Function that renders the business category pitches and its content
    """

    business_pitch = Pitch.query.filter_by(category='business').all()

    return render_template('business.html', jobs=business_pitch)