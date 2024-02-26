import flask
from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_required

from app import db
from app.main import bp
from app.main.course_filtering import filter_courses
from app.models import User, Course, Technology, School

SESSION_KEY = 'favorite'

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

    if SESSION_KEY in flask.session:
        courses_ids = flask.session[SESSION_KEY]
        courses_ids.append(course_id)
        flask.session[SESSION_KEY] = courses_ids
    else:
        flask.session[SESSION_KEY] = [course_id]
    return redirect(request.referrer)

@bp.route('/favorite', methods=['GET'])
def get_favorite():
    course_ids = flask.session.get(SESSION_KEY) if flask.session.get(SESSION_KEY) else []
    courses = []
    print(course_ids)
    for i in course_ids:
        courses.append(Course.query.get(i))
    return render_template('main/favorite.html', courses=courses)

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
    page = request.args.get('page', 1, type=int)
    selected_filters = request.form.getlist('filter')
    current_app.logger.debug(selected_filters)
    if not selected_filters:
        selected_filters = request.args.getlist('filter')
    print(selected_filters)
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
    next_url = url_for('main.courses', page=filtered_courses.next_num) \
        if filtered_courses.has_next else None
    prev_url = url_for('main.courses', page=filtered_courses.prev_num) \
        if filtered_courses.has_prev else None
    return render_template('main/list_courses.html', courses=filtered_courses.items,
                           indexed_filter_dict=indexed_filter_dict,
                           select=selected_filters,
                           next_url=next_url,
                           prev_url=prev_url,
                           page=page)


@bp.route('/course/<int:id>')
def course(id):
    page = request.args.get('page', 1, type=int)
    data: Course = Course.query.get(id)
    technologies = data.technologies.all()
    school = School.query.get(data.school_id)

    reviews = data.reviews.paginate(page, current_app.config['COURSE_PER_PAGE'], False)
    next_url = url_for('main.course', id=data.id ,page=reviews.next_num) \
        if reviews.has_next else None
    prev_url = url_for('main.course', id=data.id, page=reviews.prev_num) \
        if reviews.has_prev else None
    return render_template('main/course.html', course=data, technologies=technologies,
                           school=school,
                           reviews=reviews.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           page=page,
                           duration=data.duration)