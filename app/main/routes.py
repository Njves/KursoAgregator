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


@bp.route('/list', methods=['GET'])
def list():
    """
    Main page
    """
    query = User.query
    name = request.args.get('name', default='')
    email = request.args.get('email', default='')
    id = request.args.get('id', default='')
    users = User.query.limit(20).all()
    if name:
        users = query.filter(User.username.like(f'%{name}%')).limit(20).all()
    if email:
        users = query.filter(User.email.like(f'%{email}%')).limit(20).all()
    if id:
        users = [query.filter_by(id=id).one()]
    if name and email:
        users = query.filter(User.email.like(f'%{email}%')).filter(
            User.username.like(f'%{name}%')).limit(20).all()
    return render_template('main/list.html', users=users)


@bp.route('/custom', methods=['GET'])
def custom():
    result = db.session.query(
        Course.id.label('course_id'),
        Course.name.label('course_name'),
        Technology.title.label('technology_title'),
        School.title.label('school_name'),
        Course.price.label('course_price')
    ).join(
        course_technology, Course.id == course_technology.columns.course_id
    ).join(
        Technology, course_technology.columns.technology_id == Technology.id
    ).join(
        School, Course.school_id == School.id
    ).order_by(Course.id).limit(20).all()
    return render_template('main/custom.html', result=result)


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

    courses_data = [
    {
        'id': 1,
        'title': 'Введение в Python',
        'description': 'Освойте основы программирования на Python и начните свой путь в мир разработки.',
        'technology': 'Python'
    },
    {
        'id': 2,
        'title': 'Продвинутое программирование на Java',
        'description': 'Разберитесь с расширенными концепциями программирования на Java и создайте сложные приложения.',
        'technology': 'Java'
    },
    {
        'id': 3,
        'title': 'Разработка веб-приложений с использованием Django',
        'description': 'Научитесь создавать мощные веб-приложения, используя Django, популярный фреймворк для Python.',
        'Продолжительность': '8 недель',
        'technology': 'Python'
    },
    {
        'id': 4,
        'title': 'Основы Data Science',
        'description': 'Изучите основы анализа данных и машинного обучения с использованием Python и библиотеки Pandas.',
        'technology': 'Python'
    },
    {
        'id': 5,
        'title': 'JavaScript для начинающих',
        'description': 'Познакомьтесь с основами языка программирования JavaScript и начните создавать интерактивные веб-страницы.',
        'technology': 'JavaScript'
    },
    {
        'id': 6,
        'title': 'Разработка мобильных приложений с использованием React Native',
        'description': 'Создавайте кросс-платформенные мобильные приложения с использованием React Native и JavaScript.',
        'technology': 'React Native'
    },
    {
        'id': 7,
        'title': 'Введение в машинное обучение',
        'description': 'Погружение в основы машинного обучения с использованием Python и библиотеки Scikit-Learn.',
        'technology': 'Машинное обучение'
    }
]
    filtered_courses = [course for course in courses_data if course['technology']
                        in selected_filters] if selected_filters else courses_data

    # Фильтр по поисковому запросу
    if search_query:
        filtered_courses = [course for course in filtered_courses if search_query in course['title'].lower()]

    return render_template('main/list_courses.html', courses=filtered_courses, indexed_filter_dict=indexed_filter_dict, select=selected_filters)

@bp.route('/course/<int:id>')
def course(id):
    # Заглушка чтобы ссылки генерились хотя бы 'id'
    # ...
    pass
