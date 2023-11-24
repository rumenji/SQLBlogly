from unittest import TestCase
import datetime

from app import app
from models import db, User, Post, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


with app.app_context():
    db.drop_all()
    db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        """Clear any existing users"""
        with app.app_context():
            User.query.delete()

    def tearDown(self):
        """Rollback any not commited transactions"""
        with app.app_context():
            db.session.rollback()

    def test_user_fullname(self):
        user = User(first_name="Test", last_name="User", image_url="http://google.com")
        self.assertEqual(user.get_full_name(), "Test User")

class PostModelTestCase(TestCase):

    def setUp(self):
        """Clear any existing users"""
        with app.app_context():
            Post.query.delete()

    def tearDown(self):
        """Rollback any not commited transactions"""
        with app.app_context():
            db.session.rollback()

    def test_friendly_date(self):
        new_post = Post(title="Test Title", content="Test Content", created_at=datetime.datetime(2023, 11, 24, 13, 54, 37, 891830))
        self.assertEqual(new_post.friendly_date, 'Fri Nov 24  2023, 1:54 PM')