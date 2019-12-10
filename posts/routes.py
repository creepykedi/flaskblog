from flask import request, render_template, url_for, flash, redirect, abort, Blueprint
from flaskblog import db
from flaskblog.unpackaged.models import Post
from flask_login import login_required,  current_user
from flaskblog.posts.myforms import PostForm

# users is just name
posts = Blueprint('posts', __name__)


@posts.route('/post/new',  methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # making a post which uses forms data from html layout
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        # adding info to database
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

# making a route to a post
@posts.route('/post/<int:post_id>')
def post(post_id):
    # getting a post by number from db
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) # 403 is http forbidden route
    form = PostForm()
    # if form was valid, update post to what's in the form:
    if form.validate_on_submit():
        # html form will take those values
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated.', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        # fill the form with current values
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('main.home'))
posts