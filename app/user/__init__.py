from flask import Blueprint

bp = Blueprint('user_bp', __name__)

from app.user import routes