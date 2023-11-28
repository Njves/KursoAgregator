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
    school = School.query.filter_by(id=school_id).one()
    if not school:
        return flask.abort(status=404)
    reviews = school.reviews
    return render_template('review/review_school.html', school=school, reviews=reviews)


@bp.route('/reviews', methods=['GET'])
def reviews():
    """
    Show reviews by course id
    """
    schools = School.query.all()
    
    return render_template('review/reviews.html', schools=schools)


@login_required
@bp.route('/review/<int:course_id>', methods=['POST'])
def write_review(course_id):
    """
    Show reviews by course id
    """
    text = request.form.get('text')
    rating = request.form.get('rating')
    user_id = request.form.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login', next=request.referrer))
    if text and rating:
        review = Review(text=text, rating=rating, author_id=user_id)
        course = Course.query.filter_by(id=course_id).one()
        course.reviews.append(review)
        db.session.add(review)
        db.session.add(course)
        db.session.commit()
        flash('Отзыв успешно отправлен')
    return redirect(request.referrer)
