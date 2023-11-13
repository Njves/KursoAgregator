from flask import Blueprint

bp = Blueprint('review', __name__)

from app.review import routes