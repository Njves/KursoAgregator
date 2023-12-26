import unittest

import app
from tests.config import TestConfig


class AppCreateTest(unittest.TestCase):
    """
    Тестирует приложение
    """
    def test_app_create(self):
        """
        Проверяет фабрику приложения
        """
        self.assertFalse(app.create_app(TestConfig) is None, True)

    def test_app_create_by_different_config(self):
        """
        Проверяет фабрику с разными конфигами
        """
        class NewTestConfig:
            SQLALCHEMY_DATABASE_URI = 'sqlite://'
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            SECRET_KEY = 'test'
            TESTING = True
        self.assertFalse(app.create_app(NewTestConfig) is None)