import csv
import os
import pathlib

from app import db
from app.models import Course, Technology
from app.task import bp
__parsers_names = ['geekbrains.csv', 'hexlet.csv', 'top-academy.csv']

@bp.route('/parse', ['POST'])
def parse():
    for name in __parsers_names:
        path = pathlib.Path(os.path.abspath(os.path.dirname(__file__)), 'parsers', name)
        with open(path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            for row in csv_reader:
                link = row['URL']
                description = row['Description']
                duration = row['Duration']
                price = row['Price']
                technologies = row['Technology']
                if Course.query.filter_by(link=link).first():
                    course = Course(link=link, name=name, description=description, duration=duration, price=price)
                    for technology in technologies:
                        if Technology.query.filter_by(title=technology).first():
                            continue
                        tech = Technology(title=technology)
                        print('Добавил', tech)
                        db.session.add(tech)
                    course.technologies = technologies
                    print('Добавил', course)
                    db.session.add(course)
                    db.session.commit()

