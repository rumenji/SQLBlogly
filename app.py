"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret!'

connect_db(app)
# db.create_all()
# This doesn't work - the below does:
with app.app_context():
    db.create_all()

# from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)
@app.route("/")
def index():
    posts = Post.query.all()
    return render_template ("index.html", posts = posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404 

@app.route("/users")
def list_users():
    """List users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", users=users)

@app.route("/users/new", methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        return render_template("new_user.html")
    
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show user details."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id)
    return render_template("details.html", user=user, posts = posts)

@app.route("/users/<int:user_id>/edit", methods=['GET', 'POST'])
def edit_user(user_id):
    """Show edit user form."""
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return render_template("edit_user.html", user=user)
    
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image-url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get(post_id)

    return render_template("post_details.html", post=post)

@app.route("/users/<int:user_id>/posts/new", methods=['GET', 'POST'])
def add_post(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        return render_template('new_post.html', user=user)
    
    title = request.form['title']
    content = request.form['content']

    post = Post(title = title, content = content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>/edit", methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'GET':
        return render_template('edit_post.html', post = post)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.usr.id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')