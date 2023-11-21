from unittest import TestCase

from app import app
from models import db, User

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
