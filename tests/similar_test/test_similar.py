import unittest

from app import create_app, db
from app.models import Technology, School, Course
from tests.config import TestConfig
from app.similar import get_similar_course


class TestSimilar(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        tech1 = Technology(title="Python")
        tech5 = Technology(title="Django")
        tech6 = Technology(title="Flask")
        tech9 = Technology(title="SQL")
        school1 = School(title="Coding Academy", description="A coding school offering various courses")
        course1 = Course(name="Python for Beginners", price=99.99, rating=4.5, duration="3 months",
                         description="Learn Python programming from scratch", link="python-beginners-course")
        course1.school = school1
        course1.technologies.append(tech1)

        course2 = Course(name="Питон для начинающих", price=99.99, rating=4.5, duration="3 months",
                         description="Learn Python programming from scratch", link="python-beginners-course.xy")
        course2.school = school1
        course2.technologies.append(tech1)
        course2.technologies.append(tech5)
        course2.technologies.append(tech6)

        course3 = Course(name="Пайтон для дураков", price=99.99, rating=4.5, duration="3 months",
                         description="Learn Python programming from scratch", link="python-beginners-course.zx")
        course3.school = school1

        course3.technologies.append(tech1)
        course3.technologies.append(tech5)
        course3.technologies.append(tech6)
        db.session.add(course1)
        db.session.add(course2)
        db.session.add(course3)
        db.session.commit()

    def test_similar(self):
        with self.app_context:
            all_courses = Course.query.all()
            similar_course = get_similar_course(all_courses[0], all_courses)
            print(similar_course)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
