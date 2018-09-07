from flask import render_template,redirect,url_for, abort
from . import main
from .forms import PitchForm, UpdateProfile, CategoryForm
from ..models import Pitches, User,  Comments
from flask_login import login_required, current_user
from .. import db, photos


@main.route('/')
def index():
    """ View root page function that returns index page """

    # category = Category.get_categories(id)

    title = 'WELCOME TO ONE MINUTE PITCH'
    return render_template('index.html', title = title, )


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



# ----- TESTING HERE


#display categories on the landing page

#Route for adding a new pitch
@main.route('/category/pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def new_pitch(id):
    ''' Function to check Pitches form and fetch data from the fields '''
    form = PitchForm()
    category = Category.query.filter_by(id=id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        pitchcontent = form.pitchcontent.data
        new_pitch= Pitches(pitchcontent=pitchcontent,category_id= category.id,user_id=current_user.id)
        new_pitch.save_pitch()
        return redirect(url_for('.category', id=category.id))

    return render_template('pitch.html', pitch_form=form, category=category)

@main.route('/categories/<int:id>')
def category(id):
    category = Category.query.get(id)
    if category is None:
        abort(404)

    pitches=Pitches.get_pitches(id)
    return render_template('category.html', pitches=pitches, category=category)

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
    return render_template('new_category.html', category_form = form,title=title)

#view single pitch alongside its comments
@main.route('/view-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def view_pitch(id):
    '''
    Function the returns a single pitch for comment to be added
    '''
    print(id)
    pitches = Pitches.query.get(id)

    if pitches is None:
        abort(404)
    #
    comment = Comments.get_comments(id)
    return render_template('view-pitch.html', pitches=pitches, comment=comment, category_id=id)

#adding a comment
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    ''' function to post comments '''
    form = CommentForm()
    title = 'post comment'
    pitches = Pitch.query.filter_by(id=id).first()

    if pitches is None:
         abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comments(opinion=opinion, user_id=current_user.id, pitches_id=pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.view_pitch', id=pitches.id))

    return render_template('post_comment.html', comment_form=form, title=title)

#Routes upvoting/downvoting pitches
@main.route('/pitch/upvote/<int:id>')
@login_required
def upvote(id):
    '''
    View function that add one to the vote_number column in the votes table
    '''
    pitch_id = Pitch.query.filter_by(id=id).first()

    if pitch_id is None:
         abort(404)

    new_vote = Votes(vote=int(1), user_id=current_user.id, pitches_id=pitch_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_pitch', id=id))



@main.route('/pitch/downvote/<int:id>')
@login_required
def downvote(id):

    '''
    View function that add one to the vote_number column in the votes table
    '''
    pitch_id = Pitch.query.filter_by(id=id).first()

    if pitch_id is None:
         abort(404)

    new_vote = Votes(vote=int(2), user_id=current_user.id, pitches_id=pitch_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_pitch', id=id))

@main.route('/pitch/downvote/<int:id>')
def vote_count(id):
    '''
    View function to return the total vote count per pitch
    '''
    votes = Votes.query.filter_by(user_id=user_id, line_id=line_id).all()

    total_votes = votes.count()

    return total_votes