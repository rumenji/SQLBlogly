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




# Test posts

class TagModelTestCase(TestCase):

    def setUp(self):
        """Clear any existing posts"""
        with app.app_context():
            Post.query.delete()
            User.query.delete()
            Tag.query.delete()
            user = User(first_name="Test", last_name="User", image_url="http://google.com")
            db.session.add(user)

            post = Post(title='Post Title', content='Test post content', user=user)
            db.session.add(post)

            tag = Tag(name='Dogs')
            db.session.add(tag)

            db.session.commit()

            self.tag_id = tag.id
            print(self.tag_id)

    def tearDown(self):
        """Rollback any not commited transactions"""
        with app.app_context():
            db.session.rollback()


    def test_new_tag(self):
        with app.test_client() as client:
            t = {"name": "Fun"}
            resp = client.post(f"/tags/new", data=t, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Fun", html)

    def test_list_tags(self):
        with app.test_client() as client:
            
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Dogs', html)

    def test_delete_tags(self):
        with app.test_client() as client:
            
            resp = client.post(f"/tags/{self.tag_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Dogs", html)
        
