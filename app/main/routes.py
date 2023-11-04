from flask import render_template

from app.main import bp


@bp.route('/', methods=['GET'])
def index():
    """
    Main page
    """
    languages = ['Python', 'Golang', 'Data Science', 'Java', 'Kotlin', 'Backend', 'Unity', 'SQL', 'Fronted']
    return render_template('main/main.html', languages=languages)
