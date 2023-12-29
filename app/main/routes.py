from flask import render_template, request, redirect, url_for, current_app

from app import db, cache
from app.main import bp
from app.main.course_filtering import filter_courses
from app.models import User, Course, Technology, School, course_technology
import datetime


@bp.route('/', methods=['GET'])
@cache.cached(timeout=86100)
def index(page=1):
    """
    Main page
    """
    languages = [i.title for i in Technology.query.all()]
    languages = languages[0:9]
    return render_template('main/main.html', languages=languages, page=page)

@bp.route('/<int:page>', methods=['GET'])
@cache.cached(timeout=86100)
def index_paged(page):
    """
    Main page
    """
    languages = [i.title for i in Technology.query.all()]
    languages = languages[(page-1) * 9: page * 9]
    return render_template('main/main.html', languages=languages, page=page)

@bp.route('/next_page/<int:page>', methods=['GET'])
@cache.cached(timeout=86100)
def next_page(page):
    """
    Main page
    """
    if page+1 * 9 > len(Technology.query.all()):
        return redirect(url_for('main.index_paged', page=page))
    return redirect(url_for('main.index_paged', page=page+1))

@bp.route('/prev_page/<int:page>', methods=['GET'])
@cache.cached(timeout=86100)
def prev_page(page):
    """
    Main page
    """
    print(page < 1)
    if page-1 < 1:
        return redirect(url_for('main.index_paged', page=page))
    return redirect(url_for('main.index_paged', page=page-1))


@bp.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        id = request.form.get('id')
        User.query.filter_by(id=id).delete()
        db.session.commit()
    return redirect(url_for('main.list'))


@bp.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        u = User(username=request.form.get('username'), email=request.form.get('email'),
                 date=request.form.get('date'), last_seen=request.form.get('date'), password_hash='123456')
        db.session.add(u)
        db.session.commit()
    return redirect(url_for('main.list'))


@bp.route('/list_courses', methods=['GET'])
@cache.cached(timeout=86100)
def courses():
    page = request.args.get('page', 1, type=int)
    selected_filters = request.form.getlist('filter')
    if not selected_filters:
        selected_filters = request.args.getlist('filter')
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

    reviews = data.reviews.paginate(1, current_app.config['COURSE_PER_PAGE'], False)
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