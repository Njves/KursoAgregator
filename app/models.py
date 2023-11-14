from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

course_technology = db.Table('course_technology',
                             db.Column('course_id', db.Integer, db.ForeignKey('course.id', ondelete='CASCADE')),
                             db.Column('technology_id', db.Integer, db.ForeignKey('technology.id', ondelete='CASCADE')))

course_review = db.Table('course_review',
                         db.Column('course_id', db.Integer, db.ForeignKey('course.id', ondelete='CASCADE')),
                         db.Column('review_id', db.Integer, db.ForeignKey('review.id', ondelete='CASCADE')))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, default="")
    password_hash = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, comment='date of registation')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, comment='last seen user in online')
    reviews = db.relationship('Review', backref='owner', lazy='dynamic')
    def __repr__(self) -> str:
        return f'User {self.id}, Username: {self.username}, email: {self.email}, date: {self.date},' \
               f' last_seen: {self.last_seen}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Double, nullable=False)
    rating = db.Column(db.Float)
    duration = db.Column(db.Float)
    date_start = db.Column(db.DateTime, default=datetime.utcnow)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete='CASCADE'))
    link = db.Column(db.String(256), nullable=False)
    reviews = db.relationship('Review', backref='review', secondary=course_review,
                              lazy='dynamic')
    technologies = db.relationship('Technology', backref='technologies', secondary=course_technology,
                                   lazy='dynamic')

    def __repr__(self) -> str:
        return f'Course {self.id}, name: {self.name}, price: {self.price}, date_start: {self.date_start},' \
               f' link: {self.link}'


class Technology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    text = db.Column(db.String)
    rating = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Review {self.id}, user_id: {self.user_id}, text: {self.text}, rating: {self.rating},' \
               f' date: {self.date}'
