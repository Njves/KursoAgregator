from flask import render_template, request, redirect, url_for

from app import db
from app.main import bp
from app.main.course_filtering import filter_courses
from app.models import User, Course, Technology, School, course_technology
import datetime


@bp.route('/', methods=['GET'])
def index():
    """
    Main page
    """
    languages = [i.title for i in Technology.query.all()]
    languages = languages[0:9]
    return render_template('main/main.html', languages=languages)


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
def courses():
    selected_filters = request.form.getlist('filter')
    if not selected_filters:
        selected_filters = request.args.getlist('filter')
    unique_technologies = Technology.query.with_entities(
        Technology.title).distinct().all()
    unique_schools = School.query.with_entities(School.title).distinct().all()
<<<<<<< HEAD
    filter_dict = {
        'Направления': [tech[0] for tech in unique_technologies],
        'Школа': [school[0] for school in unique_schools],
=======
    unique_durations = Course.query.with_entities(
        Course.duration).distinct().all()
    sorted_durations = sorted(set(
        duration[0] for duration in unique_durations), key=lambda x: int(x.split()[0]))
    filter_dict = {
        'Направления': [tech[0] for tech in unique_technologies],
        'Школа': [school[0] for school in unique_schools],
        'Длительность': sorted_durations,
>>>>>>> main
    }
    indexed_filter_dict = enumerate(filter_dict.items())
    filtered_courses = filter_courses(filter_dict, selected_filters)
    return render_template('main/list_courses.html', courses=filtered_courses, indexed_filter_dict=indexed_filter_dict, select=selected_filters)


@bp.route('/course/<int:id>')
def course(id):
    data = Course.query.get(id)
    technologies = data.technologies.all()
    school = School.query.get(data.school_id)
    return render_template('main/course.html', course=data, technologies=technologies, school=school)
