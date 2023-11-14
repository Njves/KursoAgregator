from flask import render_template

from app.review import bp


@bp.route('/<int:course_id>/reviews', methods=['GET'])
def review(course_id):
    """
    Show reviews by course id
    """

    return render_template('review/review.html')


@bp.route('/reviews', methods=['GET'])
def review(course_id):
    """
    Show reviews by course id
    """

    return render_template('review/review.html')