from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
"""Models for Blogly."""

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key = True,
                   autoincrement=True)
    first_name = db.Column(db.String(20),
                           nullable=False
                           )
    last_name = db.Column(db.String(20),
                           nullable=False
                           )
    image_url = db.Column(db.Text,
                          nullable=True)
    
    def __repr__(self) -> str:
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                   primary_key = True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable = False)
    content = db.Column(db.Text,
                        nullable = False)
    created_at = db.Column(db.DateTime,
                           nullable = False,
                           default = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    @property
    def friendly_date(self):

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")