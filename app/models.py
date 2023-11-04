import uuid
from datetime import datetime

from app import db


course_technology = db.Table('Course_Technology',
                             db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
                             db.Column('technology_id', db.Integer, db.ForeignKey('technology.id')))

course_review = db.Table('Course_Review',
                         db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
                         db.Column('review_id', db.Integer, db.ForeignKey('review.id')))
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False, default="")
    password_hash = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, comment='date of registation')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, comment='last seen user in online')
    reviews = db.relationship('Review', backref='owner', lazy='dynamic')


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Double, nullable=False)
    rating = db.Column(db.Float)
    duration = db.Column(db.Float)
    date_start = db.Column(db.DateTime, default=datetime.utcnow)
    school = db.Column(db.Integer, db.ForeignKey('school.id'))
    link = db.Column(db.String(256), nullable=False)
    reviews = db.relationship('Review', backref=db.backref('reviews', lazy='dynamic'), secondary=course_review, lazy='dynamic')


class Technology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    courses = db.relationship('Course', backref='owner', lazy='dynamic')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String)
    rating = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)


