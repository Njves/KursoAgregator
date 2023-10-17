from flask import render_template

from app.main import bp


@bp.route('/', methods=['GET'])
def index():
    """
    Main page
    """
    return render_template('main/main.html')
