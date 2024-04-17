import flask
from flask import render_template, request, redirect, url_for, make_response, flash
from flask_login import login_required

from app import db
from app.models import Course, School, Review
from app.review import bp


@bp.route('/course/<int:course_id>/reviews', methods=['GET'])
def review_by_course_id(course_id):
    """
    Show reviews by course id
    """
    course = Course.query.filter_by(id=course_id).one()
    if not course:
        return flask.abort(status=404)
    reviews = course.reviews
    return render_template('review/review.html', course=course, reviews=reviews)


@bp.route('/school/<int:school_id>/reviews', methods=['GET'])
def review_by_school_id(school_id):
    """
    Show reviews by course id
    """
    school = School.query.filter_by(id=school_id).first()
    if not school:
        return flask.abort(status=404)
    reviews = [i for i in school.reviews]
    school_rating = 0
    if reviews:
        school_rating = round(sum([review.rating for review in reviews]) / len(reviews), 2)
    return render_template('review/review_school.html', school=school, reviews=reviews, school_rating=school_rating)


@bp.route('/reviews', methods=['GET'])
def reviews():
    """
    Show reviews by course id
    """
    reviews = Review.query.all()
    return render_template('review/reviews.html', reviews=reviews)


@login_required
@bp.route('/review/<int:course_id>', methods=['POST'])
def write_review(course_id):
    """
    Show reviews by course id
    """
    text = request.form.get('text')
    rating = request.form.get('rating')
    user_id = request.form.get('user_id')
    if len(text) > 1024:
        return redirect(request.referrer)
    if not user_id:
        return redirect(url_for('auth.login', next=request.referrer))
    if text and rating:
        review = Review(text=text, rating=rating, author_id=user_id)
        course = Course.query.filter_by(id=course_id).one()
        course.reviews.append(review)
        school = School.query.filter_by(id=course.school_id).first()
        if school:
            school.reviews.append(review)
        db.session.add(review)
        db.session.add(course)
        db.session.commit()
        flash('Отзыв успешно отправлен')
    return redirect(request.referrer)
