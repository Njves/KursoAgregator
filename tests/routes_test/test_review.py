import unittest

from app import create_app, db
from app.models import Review, Course, School, User, Technology
from course_filtering import filter_courses
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
        tech1 = Technology(title="Python")
        tech2 = Technology(title="JavaScript")
        tech3 = Technology(title="React")
        tech4 = Technology(title="Vue.js")
        tech5 = Technology(title="Django")
        tech6 = Technology(title="Flask")
        tech7 = Technology(title="HTML")
        tech8 = Technology(title="CSS")
        tech9 = Technology(title="SQL")
        tech10 = Technology(title="Git")

        # Creating instances of School
        school1 = School(title="Coding Academy", description="A coding school offering various courses")
        school2 = School(title="Web Dev Institute", description="Specializing in web development education")
        school3 = School(title="Tech Masters", description="Empowering tech enthusiasts through education")

        # Creating instances of User
        user1 = User(username="john_doe")
        user1.set_password("password123")

        user2 = User(username="jane_doe")
        user2.set_password("securepass")

        # Creating instances of Course
        course1 = Course(name="Python for Beginners", price=99.99, rating=4.5, duration="3 months",
                         description="Learn Python programming from scratch", link="python-beginners-course")
        course1.school = school1

        course2 = Course(name="Web Development Bootcamp", price=149.99, rating=4.8, duration="6 months",
                         description="Comprehensive web development training", link="web-dev-bootcamp")
        course2.school = school2

        # Creating instances of Review
        review1 = Review(author=user1, text="Great course, highly recommended!", rating=4.5)
        review2 = Review(author=user2, text="Excellent content and instructors", rating=4.8)

        # Assigning reviews to courses
        course1.reviews.append(review1)
        course1.reviews.append(review2)
        course2.reviews.append(review1)
        course2.reviews.append(review2)

        # Committing changes to the database
        db.session.add_all([tech1, tech2, tech3, tech4, tech5, tech6, tech7, tech8, tech9, tech10,
                            school1, school2, school3,
                            user1, user2,
                            course1, course2,
                            review1, review2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_review(self):
        with self.app.test_request_context('/?price_from=100&price_to=200&duration_from=3&duration_to=6&search=Course&selected_filters[]=School A&selected_filters[]=Tech A'):
            course = Course.query.all()[0]
            user1 = User(username="john_doe")
            user1.set_password("password123")
            review1 = Review(author=user1, text="Great course, highly recommended!", rating=4.5)
            course.reviews.append(review1)
            self.assertEqual(course.reviews[-1], review1)
