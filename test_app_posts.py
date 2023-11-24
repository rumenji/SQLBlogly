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

class PostModelTestCase(TestCase):

    def setUp(self):
        """Clear any existing posts"""
        with app.app_context():
            Post.query.delete()
            user = User(first_name="Test", last_name="User", image_url="http://google.com")
            db.session.add(user)
            db.session.commit()

            post = Post(title='Post Title', content='Test post content', user=user)
            db.session.add(post)
            db.session.commit()

            self.user_id = user.id
            self.post_id = post.id
            

            

    def tearDown(self):
        """Rollback any not commited transactions"""
        with app.app_context():
            db.session.rollback()


    def test_new_post(self):
        with app.test_client() as client:
            p = {"title": "Post Title 2", "content": "Test post 2 content"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=p, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post Title 2", html)

    def test_list_posts(self):
        with app.test_client() as client:
           
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Post Title', html)

    def test_delete_post(self):
        with app.test_client() as client:
            
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Post Title", html)