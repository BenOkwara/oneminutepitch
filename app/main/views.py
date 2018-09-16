from flask import render_template, request, redirect,url_for, abort, flash
from . import main
from .forms import PitchForm, UpdateProfile, CommentForm
from ..models import Pitch, User, Comment
from flask_login import login_required, current_user
from .. import db, photos
import markdown2

# INDEX PAGE
@main.route('/')
def index():
    """ View root page function that returns index page """

    # category = Category.get_categories()
    pitches = Pitch.query.all()

    title = 'WELCOME TO ONE MINUTE PITCH'
    return render_template('index.html', title = title, pitches=pitches)

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
    user = User.query.filter_by(username=uname).first()
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

# ADDING A NEW PITCH
@main.route('/pitch/new', methods=['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()

    if form.validate_on_submit():

        title=form.title.data
        content=form.content.data
        category_id=form.category_id.data
        pitch = Pitch(title=title,
                      content=content,
                      category_id=category_id,
                      user=current_user)

        db.session.add(pitch)
        db.session.commit()

        # pitch.save_pitch(pitch)
        print('kasambuli')
        flash('Your pitch has been created!', 'success')
        return redirect(url_for('main.single_pitch',id=pitch.id))

    return render_template('newpitch.html', title='New Post', pitch_form=form, legend='New Post')

# VIEW INDIVIDUAL PITCH
@main.route('/pitch/new/<int:id>')
def single_pitch(id):
    pitch = Pitch.query.get(id)
    return render_template('singlepitch.html',pitch = pitch)

@main.route('/allpitches')
def pitch_list():
    # Function that renders the business category pitches and its content

    pitches = Pitch.query.all()

    return render_template('pitches.html', pitches=pitches)


# VIEWING A PITCH WITH COMMENTS AND COMMENTFORM
@main.route('/pitch/<int:pitch_id>/',methods=["GET","POST"])
def pitch(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    form = CommentForm()
    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data
        new_pitch_comment = Comment(post_comment=comment,
                                    pitches=pitch_id,

                                    # user_id=current_user.id,
                                    user=current_user)
        # new_post_comment.save_post_comments()


        db.session.add(new_pitch_comment)
        db.session.commit()
    comments = Comment.query.all()
    return render_template('pitchlink.html', title=pitch.title,
                           pitch=pitch,
                           pitch_form=form,
                           comments=comments)

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

# UPDATING A PITCH

@main.route('/pitch/<int:pitch_id>/update', methods=['GET','POST'])
@login_required
def update_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if pitch.author != current_user:
        abort(403)
    form = PitchForm()
    if form.validate_on_submit():
        pitch.title = form.title.data
        pitch.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.pitchlink', pitch_id=pitch.id))
    elif request.method == 'GET':
        form.title.data = pitch.title
        form.content.data = pitch.content
    return render_template('newpitch.html', title='Update Pitch', form=form, legend='Update Pitch')

# DELETING A PITCH
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

# VIEWING A SPECIFIC PITCH
@main.route("/view/<id>", methods=["GET","POST"])
def view_pitch(id):
    pitch = Pitch.query.get(id)
    if request.args.get("vote"):
       pitch.likes = pitch.likes + 1
       pitch.save_pitch()
       return redirect("/view/{pitch_id}".format(pitch_id=id))
    return render_template('viewpitch.html',pitch = pitch)