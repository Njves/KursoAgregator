from flask import render_template, request, redirect, url_for

from app import db
from app.main import bp
from app.models import User


@bp.route('/', methods=['GET'])
def index():
    """
    Main page
    """
    languages = ['Python', 'Golang', 'Data Science', 'Java',
                 'Kotlin', 'Backend', 'Unity', 'SQL', 'Fronted']
    return render_template('main/main.html', languages=languages)