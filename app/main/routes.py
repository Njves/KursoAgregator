import flask
from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from app import db, similar
from app.main import bp
from app.main.course_filtering import filter_courses
from app.main.hours_to_time import format_time
from app.models import User, Course, Technology, School
from app.similar import get_similar_course

@bp.route('/', methods=['GET'])
def index():
    """
    Main page
    """
    page = request.args.get('page', 1, type=int)
    languages = Technology.query.paginate(page, current_app.config['TECHNOLOGY_PER_PAGE'], False)
    next_url = url_for('main.index', page=languages.next_num) \
        if languages.has_next else None
    prev_url = url_for('main.index', page=languages.prev_num) \
        if languages.has_prev else None
    languages = [i.title for i in languages.items]
    return render_template('main/main.html', languages=languages, page=page, next_url=next_url, prev_url=prev_url)


@bp.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        id = request.form.get('id')
        User.query.filter_by(id=id).delete()
        db.session.commit()
    return redirect(url_for('main.list'))


@login_required
@bp.route('/favorite', methods=['POST'])
def add_favorite():
    course_id = request.form.get('course_id')
    if course := Course.query.filter_by(id=course_id).first():
        current_user.favorite_courses.append(course)
        db.session.add(current_user)
        db.session.commit()
    else:
        return flask.abort(404)
    return redirect(request.referrer)

@login_required
@bp.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    course_id = request.form.get('course_id')
    if course := Course.query.filter_by(id=course_id).first():
        current_user.favorite_courses.remove(course)
        db.session.add(current_user)
        db.session.commit()
    else:
        return flask.abort(404)
    return redirect(request.referrer)


@bp.route('/favorite', methods=['GET'])
def get_favorite():
    page = request.args.get('page', 1, type=int)
    selected_filters = request.form.getlist('filter')
    current_app.logger.debug(selected_filters)
    if not selected_filters:
        selected_filters = request.args.getlist('filter')
    current_app.logger.debug(selected_filters)
    unique_technologies = Technology.query.with_entities(
        Technology.title).distinct().all()
    unique_schools = School.query.with_entities(School.title).distinct().all()
    filter_dict = {
        'Направления': [tech[0] for tech in unique_technologies],
        'Школа': [school[0] for school in unique_schools]
    }
    indexed_filter_dict = enumerate(filter_dict.items())
    filtered_courses = filter_courses(filter_dict, selected_filters, current_user.favorite_courses).order_by(Course.date_start.desc())
    filtered_courses = filtered_courses.paginate(page, current_app.config['COURSE_PER_PAGE'], False)
    for course in filtered_courses.items:
        course.duration = format_time(int(course.duration))
    filters = {
        'search': request.args.get('search'),
        'sort_by': request.args.get('sort_by'),
        'filter': selected_filters,
        'duration_from': request.args.get('duration_from'),
        'duration_to': request.args.get('duration_to'),
        'price_from': request.args.get('price_from'),
        'price_to': request.args.get('price_to')
    }
    next_url = url_for('main.get_favorite', **filters, page=filtered_courses.next_num,  ) \
        if filtered_courses.has_next else None
    prev_url = url_for('main.get_favorite',  **filters, page=filtered_courses.prev_num) \
        if filtered_courses.has_prev else None
    return render_template('main/favorite.html', courses=filtered_courses.items,
                           indexed_filter_dict=indexed_filter_dict,
                           select=selected_filters,
                           next_url=next_url,
                           prev_url=prev_url,
                           page=page)



@bp.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        u = User(username=request.form.get('username'), email=request.form.get('email'),
                 date=request.form.get('date'), last_seen=request.form.get('date'), password_hash='123456')
        db.session.add(u)
        db.session.commit()
    return redirect(url_for('main.list'))


@bp.route('/list_courses', methods=['GET'])
def courses():
    favs = []
    if hasattr(current_user, 'favorite_courses'):
        favs = [course.id for course in current_user.favorite_courses]
    page = request.args.get('page', 1, type=int)
    selected_filters = request.form.getlist('filter')
    current_app.logger.debug(selected_filters)
    if not selected_filters:
        selected_filters = request.args.getlist('filter')
    current_app.logger.debug(selected_filters)
    unique_technologies = Technology.query.with_entities(
        Technology.title).distinct().all()
    unique_schools = School.query.with_entities(School.title).distinct().all()
    filter_dict = {
        'Направления': [tech[0] for tech in unique_technologies],
        'Школа': [school[0] for school in unique_schools]
    }
    indexed_filter_dict = enumerate(filter_dict.items())
    filtered_courses = filter_courses(filter_dict, selected_filters).order_by(Course.date_start.desc())
    filtered_courses = filtered_courses.paginate(page, current_app.config['COURSE_PER_PAGE'], False)
    for course in filtered_courses.items:
        course.duration = format_time(int(course.duration))
    filters = {
        'search': request.args.get('search'),
        'sort_by': request.args.get('sort_by'),
        'filter': selected_filters,
        'duration_from': request.args.get('duration_from'),
        'duration_to': request.args.get('duration_to'),
        'price_from': request.args.get('price_from'),
        'price_to': request.args.get('price_to')
    }
    next_url = url_for('main.courses', **filters, page=filtered_courses.next_num ) \
        if filtered_courses.has_next else None
    prev_url = url_for('main.courses', **filters, page=filtered_courses.next_num ) \
        if filtered_courses.has_prev else None
    return render_template('main/list_courses.html', courses=filtered_courses.items,
                           indexed_filter_dict=indexed_filter_dict,
                           select=selected_filters,
                           favs=favs,
                           next_url=next_url,
                           prev_url=prev_url,
                           page=page)


@bp.route('/course/<int:id>')
def course(id):
    favs = []
    if hasattr(current_user, 'favorite_courses'):
        favs = [course.id for course in current_user.favorite_courses]
    page = request.args.get('page', 1, type=int)
    data: Course = Course.query.get(id)
    technologies = data.technologies.all()
    school = School.query.get(data.school_id)
    duration = format_time(int(data.duration))
    source = Course.query.get(id)
    if not source:
        return []
    technology_ids = [tech.id for tech in source.technologies]
    courses_by_technologies = Course.query.join(Course.technologies).filter(Technology.id.in_(technology_ids)).all()

    similars = get_similar_course(source, courses_by_technologies)

    reviews = data.reviews.paginate(page, current_app.config['COURSE_PER_PAGE'], False)
    next_url = url_for('main.course', id=data.id, page=reviews.next_num) \
        if reviews.has_next else None
    prev_url = url_for('main.course', id=data.id, page=reviews.prev_num) \
        if reviews.has_prev else None
    return render_template('main/course.html', course=data, technologies=technologies,
                           school=school,
                           reviews=reviews.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           page=page,
                           favs=favs,
                           duration=duration,
                           similars=similars)
