import ast
import csv
import pathlib
from typing import List

from flask import Response, current_app, render_template
from sqlalchemy import text

from app import db
from app.auth.emal import send_email
from app.models import Course, Technology, School, User
from app.task import bp
from app.task.validate import validate_data
from config import basedir


def init(app):
    with app.app_context():
        schools = [School(title='Geekbrains'), School(title='Hexlet'), School(title='Stepik'),
                   School(title='TopAcademy')]
        [db.session.add(school) for school in schools]
        db.session.commit()


def get_school(app):
    with app.app_context():
        return School.query.filter_by(title='Geekbrains').first(), School.query.filter_by(title='Hexlet').first(),\
            School.query.filter_by(title='Stepik').first(),\
            School.query.filter_by(title='TopAcademy').first()

@bp.route('/parse', methods=['POST', ])
def parse():
    """
    Ручка для парсинга файлов .csv с курсами
    :return: Response(200) - если все успешно добавлено
    """
    current_app.logger.info('Запросили парсинг')
    if any(school is None for school in get_school(current_app)):
        init(current_app)
    __parsers_names = {School.query.filter_by(title='Geekbrains').first(): 'geekbrains.csv',
                       School.query.filter_by(title='Hexlet').first(): 'hexlet.csv',
                       School.query.filter_by(title='Stepik').first(): 'stepik.csv',
                       School.query.filter_by(title='TopAcademy').first(): 'top-academy.csv'}

    # print('Начинаю парсинг')
    # geekbrains_parser_courses_parallel()
    # hexlet_parser_courses_parallel()
    # top_academy_parser_courses_parallel()
    # stepik_parser_courses_parallel()
    # print('Закончил парсинг')
    validate_data()
    for school, file_name in __parsers_names.items():
        path = pathlib.Path(basedir, 'app', 'parsers', file_name)
        with open(path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            for row in csv_reader:
                if row.get('URL', False):
                    link: str = row['URL']
                else:
                    continue
                if row.get('Name', False):
                    name: str = row['Name']
                if row.get('Description', False):
                    description: str = row['Description']
                if row.get('Duration', False):
                    duration: str = row['Duration']
                if row.get('Price', False):
                    price = float(row['Price'])
                if row.get('Technology'):
                    technologies: list[str] = ast.literal_eval(row['Technology'])
                appended_technologies: list[Technology] = []
                # Если курса есть в бд, обновляем данные
                existing_course = Course.query.filter_by(link=link).first()
                if existing_course:
                    existing_course.name = name
                    existing_course.description = description
                    existing_course.duration = duration
                    existing_course.price = price
                    existing_course.technologies = []
                    appended_technologies = []
                    for technology in technologies:
                        if technology_from_db := Technology.query.filter_by(title=technology).first():
                            appended_technologies.append(technology_from_db)
                            continue
                        appended_technologies.append(add_technology(technology))
                    if appended_technologies:
                        existing_course.technologies = appended_technologies
                    # Коммитим изменения в базу данных
                    db.session.commit()
                    print('Обновил', existing_course)
                else:
                    # Если курса нет в базе данных, добавляем новый кур
                    course = Course(link=link, name=name, description=description, duration=duration, price=price,
                                    school_id=school.id)
                    for technology in technologies:
                        if technology_from_db := Technology.query.filter_by(title=technology).first():
                            appended_technologies.append(technology_from_db)
                            continue
                        appended_technologies.append(add_technology(technology))
                    if appended_technologies:
                        course.technologies = appended_technologies
                    print('Добавил', course)
                    db.session.add(course)
                    db.session.commit()
    return Response(status=200)

@bp.route('/notify', methods=['GET'])
def notify_subscribed_users():
    # new_courses: List[Course] = Course.query.limit(10).all()
    # query = """SELECT technology_id, u.email FROM subscribe_user_technology JOIN "user" u on u.id = subscribe_user_technology.user_id ORDER BY technology_id;"""
    # result = db.session.execute(query).fetchall()
    # technologies = (technology_id for technology_id, email in result)
    # bindEmails = {}
    # for technology_id, email in result:
    #     if technology_id in result:
    #         bindEmails[technology_id].append(email)
    #     else:
    #         bindEmails[technology_id] = [email]
    # emails = {}
    # for course in new_courses:
    #     if any([technology_id in technologies for technology_id in course.technologies]):
    #         for technology_id in course.technologies:
    #             emails = [bindEmails[technology_id]]
    #
    emails = {}
    emails['mrpostik@gmail.com'] = [Course.query.all()[0:10]]
    for receiver, courses in emails.items():
        send_mail(receiver, courses)

    return {}, 200



def send_mail(receiver_email: str, courses: List[Course]):
    send_email('[KursoAgreagator] Подписка',
               sender=current_app.config['ADMINS'][0],
               recipients=[receiver_email],
               text_body=None,
               html_body=render_template('email/new_courses_message.html', receiver_email=receiver_email, courses=courses))

def add_technology(title: str):
    technology = Technology(title=title)
    print('Добавил', technology)
    db.session.add(technology)
    return technology
