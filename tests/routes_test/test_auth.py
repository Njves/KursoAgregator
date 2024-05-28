import unittest

from flask import url_for

from app import create_app, db
from app.models import User
from tests.config import TestConfig


class TestRegistration(unittest.TestCase):
    """
        Тестирование регистрации
        """

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration(self):
        data = {
            "username": "test_user",
            "password": "password123",
            "password_repeat": "password123",
            "email": "test@example.com"
        }
        response = self.client.post(url_for('auth.register', _external=True), data=data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url_for('auth.register'))
        self.assertEqual(response.status_code, 200)

    def test_registration_failed_email_invalid(self):
        data = {"username": "test_user", "password": "password123", "password_repeat": 'password123',
                "email": "test"}
        response = self.client.post(url_for('auth.register'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_registration_failed_user_already_exists(self):
        data = {"username": "test_user2", "password": "password123", "password_repeat": 'password123', "email": "test1"}
        account = User(username='test_user')
        account.set_password('test')
        db.session.add(account)
        db.session.commit()
        error_response = self.client.post(url_for('auth.register'), data=data)
        self.assertEqual(error_response.status_code, 302)

    def test_registration_failed_password_not_same(self):
        data = {"username": "test_user", "password": "password123", "password_repeat": 'password123',
                "email": "test2"}
        response = self.client.post(url_for('auth.register'), data=data)
        self.assertEqual(response.status_code, 302)


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.account = User(username='Test')
        self.account.set_password('test')
        db.session.add(self.account)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_success(self):
        # By password
        response = self.client.post(url_for('auth.login'), data={'username': 'Test', 'password': 'test'})
        self.assertEqual(response.status_code, 302)
        # By email
        response = self.client.post(url_for('auth.login'), data={'username': 'Test@gmail.com', 'password': 'test'})
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_username_or_email(self):
        response = self.client.post(url_for('auth.login'), data={'username': 'invalid', 'password': 'test'})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(url_for('auth.login'), data={'username': 'invalid@gmail.com', 'password': 'test'})
        self.assertEqual(response.status_code, 302)
