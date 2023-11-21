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
            user = User(first_name="Test", last_name="User", image_url="http://google.com")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        """Rollback any not commited transactions"""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)

    def test_new_user(self):
        with app.test_client() as client:
            u = {"first-name": "John", "last-name": "Doe", "image-url": "http://google.com"}
            resp = client.post("/users/new", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John Doe", html)

    def test_delete_user(self):
        with app.test_client() as client:
            
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test User", html)