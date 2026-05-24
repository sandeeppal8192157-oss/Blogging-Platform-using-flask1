import unittest
from app import create_app, db
from app.models import User, Post

class BloggingPlatformTestCase(unittest.TestCase):
    def setUp(self):
        # 1. Initialize the app exactly how your code expects (0 arguments)
        self.app = create_app()
        
        # 2. Inject our test configurations directly into the active app object
        self.app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
            WTF_CSRF_ENABLED=False,
            SECRET_KEY='test-secret-key'
        )
        
        # 3. Establish the app context and build the temporary in-memory database
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        response = self.client.post('/login', data=dict(
            email='wrong@test.com',
            password='badpassword'
        ), follow_redirects=True)
        self.assertIn(b'Login Unsuccessful', response.data)

if __name__ == '__main__':
    unittest.main()