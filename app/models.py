from datetime import datetime
from time import time

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login_manager

course_technology = db.Table('course_technology',
                             db.Column('course_id', db.Integer, db.ForeignKey('course.id', ondelete='CASCADE')),
                             db.Column('technology_id', db.Integer, db.ForeignKey('technology.id', ondelete='CASCADE')))

course_review = db.Table('course_review',
                         db.Column('course_id', db.Integer, db.ForeignKey('course.id', ondelete='CASCADE')),
                         db.Column('review_id', db.Integer, db.ForeignKey('review.id', ondelete='CASCADE')))

school_review = db.Table('school_review',
                         db.Column('school_id', db.Integer, db.ForeignKey('school.id', ondelete='CASCADE')),
                         db.Column('review_id', db.Integer, db.ForeignKey('review.id', ondelete='CASCADE')))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    text = db.Column(db.String(1024))
    rating = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self) -> str:
        return f'Review {self.id}, user_id: {self.author_id}, text: {self.text}, rating: {self.rating},' \
               f' date: {self.date}'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, default="")
    password_hash = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, comment='date of registation')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, comment='last seen user in online')
    reviews = db.relationship('Review', backref='author', lazy='dynamic')

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            account = User.query.get(jwt.decode(token, current_app.config['SECRET_KEY'],
                                                   algorithms=['HS256'])['reset_password'])
            return account
        except jwt.InvalidTokenError as e:
            print(e)
            # TODO: Добавить логирование
            return

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
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float)
    duration = db.Column(db.String(128))
    description = db.Column(db.String(), nullable=False)
    date_start = db.Column(db.DateTime, default=datetime.utcnow)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id', ondelete='CASCADE'))
    link = db.Column(db.String(256), nullable=False, unique=True)
    reviews = db.relationship('Review', backref='course', secondary=course_review,
                              lazy='dynamic')
    technologies = db.relationship('Technology', backref='tech', secondary=course_technology,
                                   lazy='dynamic')

    def __repr__(self) -> str:
        return f'Course {self.id}, name: {self.name}, price: {self.price}, date_start: {self.date_start},' \
               f' link: {self.link}'

    def to_dict(self):
        return {'id': self.id, 'name': self.name,  'price': self.price, 'date_start': self.date_start, 'link': self.link}


class Technology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'Технология: {self.id}, название: {self.title}'

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String())
    reviews = db.relationship('Review', backref='school', secondary=school_review,
                              lazy='dynamic')
    courses = db.relationship('Course', backref='owner',
                              lazy='dynamic')


    def __repr__(self):
        return f'Школа: {self.id}, название: {self.title}'
