"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User


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
    return redirect ("/users")

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
    return render_template("details.html", user=user)

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
