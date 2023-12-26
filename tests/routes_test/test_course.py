import unittest

from app import create_app, db
from tests.config import TestConfig


class TestRegistration(unittest.TestCase):
    """
        Тестирование мемов
        """

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        courses = [Course()]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

