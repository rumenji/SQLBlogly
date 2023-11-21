from flask_sqlalchemy import SQLAlchemy

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
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"