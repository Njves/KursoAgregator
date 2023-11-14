from flask import render_template, request, redirect, url_for

from app import db
from app.main import bp
from app.models import User, Course, Technology, School, course_technology
import datetime


@bp.route('/', methods=['GET'])
def index():
    """
    Main page
    """
    languages = ['Python', 'Golang', 'Data Science', 'Java',
                 'Kotlin', 'Backend', 'Unity', 'SQL', 'Fronted']
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

@bp.route('/list_courses', methods=['GET', 'POST'])
def courses():
    """Уберу все лишнее в след спринте"""
    if request.method == 'POST':
        # Обработка формы фильтров
        selected_filters = request.form.getlist('filter')
        print(selected_filters)
    else:
        # Обработка запроса GET (возможно, уже существующие фильтры)
        selected_filters = request.args.getlist('filter')
    #прикрутить фильтрацию по цене
    price_from = request.form.get('price_from')
    price_to = request.form.get('price_to')
    search_query = request.args.get('search', '').lower()
    filter_dict = {
        'Направления': ['Python', 'Golang', 'Data Science', 'Java',
                 'Kotlin', 'Backend', 'Unity', 'SQL', 'Fronted'],
        'Школа': ['Stepik', 'Hexlet', 'Geekbrains', 'TOP-academy'],
        'Длительность': ['3 месяца', '6 месяцев', '9 месяцев', '12 месяцев'],
    }
    indexed_filter_dict = enumerate(filter_dict.items())

    courses_data = Course.query.all()
    # filtered_courses = [course for course in courses_data if course.technologies[0]
    #                     in selected_filters] if selected_filters else courses_data
    filtered_courses = courses_data
    # Фильтр по поисковому запросу
    if search_query:
        filtered_courses = [course for course in filtered_courses if search_query in course['title'].lower()]

    return render_template('main/list_courses.html', courses=filtered_courses, indexed_filter_dict=indexed_filter_dict, select=selected_filters)

@bp.route('/course/<int:id>')
def course(id):
    data = Course.query.get(id)
    return render_template('main/course.html', course=data)