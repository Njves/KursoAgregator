import ast
import csv
import pathlib

from flask import Response

from app import db
from app.models import Course, Technology, School
from app.task import bp
from app.task.validate import validate_data
from config import basedir


@bp.route('/parse', methods=['POST', ])
def parse():
    """
    Ручка для парсинга файлов .csv с курсами
    :return: Response(200) - если все успешно добавлено
    """
    validate_data()
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
    links = [course.link for course in Course.query.all()]
    for school, file_name in __parsers_names.items():
        path = pathlib.Path(basedir, 'app', 'parsers', file_name)
        with open(path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            for row in csv_reader:
                if row['URL']:
                    link: str = row['URL']
                if row['Name']:
                    name: str = row['Name']
                if row['Description']:
                    description: str = row['Description']
                if row['Duration']:
                    duration: str = row['Duration']
                if row['Price']:
                    price: int = int(''.join([i for i in row['Price'] if i.isnumeric()]))
                if row['Technology']:
                    technologies: list[str] = ast.literal_eval(row['Technology'])

                appended_technologies: list[Technology] = []
                # Если курса нет в бд, формируем модельку
                if not link in links:
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


def add_technology(title: str):
    technology = Technology(title=title)
    print('Добавил', technology)
    db.session.add(technology)
    return technology
