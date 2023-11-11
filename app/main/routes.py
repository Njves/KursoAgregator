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
    languages = ['Python', 'Golang', 'Data Science', 'Java', 'Kotlin', 'Backend', 'Unity', 'SQL', 'Fronted']
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
        users = query.filter(User.email.like(f'%{email}%')).filter(User.username.like(f'%{name}%')).limit(20).all()
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