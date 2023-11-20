import flask
from flask import render_template

from app.models import Course, School
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
    return render_template('review/review.html', school=school, reviews=reviews)


@bp.route('/reviews', methods=['GET'])
def all_reviews(course_id):
    """
    Show reviews by course id
    """

    return render_template('review/review.html')
