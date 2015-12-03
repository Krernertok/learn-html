import unittest
from app.models import User
from app import db, create_app


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='python')
        return self.assertTrue(u.password_hash is not None)

    def test_verify_correct_password(self):
        u = User(password='python')
        self.assertTrue(u.verify_password('python'))

    def test_verify_incorrect_password(self):
        u = User(password='python')
        self.assertFalse(u.verify_password('boa'))

    def test_access_password_attribute(self):
        u = User(password='python')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_salts(self):
        u1 = User(password="python")
        u2 = User(password="boa")
        self.assertTrue(u1.password_hash != u2.password_hash)

    def test_confirm_token(self):
        u1 = User(password='python')
        u2 = User(password='boa')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertFalse(u1.confirmed)

        token1 = u1.generate_confirmation_token()
        token2 = u2.generate_confirmation_token()
        
        self.assertTrue(u1.confirm(token1))
        self.assertTrue(u1.confirmed)
        self.assertFalse(u1.confirm(token2))
        self.assertFalse(u1.confirm('123'))
