import os

from flask import Flask
from flask_admin import Admin
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import MetaData
import logging
from logging.handlers import RotatingFileHandler
from config import Config

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=convention))
migrate = Migrate()
login_manager = LoginManager()
admin_app = Admin(name='KursoAgregator', template_mode='bootstrap3')
login_manager.login_view = 'auth.login'
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    migrate.init_app(app, db,render_as_batch=True)
    login_manager.init_app(app)
    db.init_app(app)
    admin_app.init_app(app)
    cache.init_app(app)
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.review import bp as review_bp

    app.register_blueprint(review_bp)

    from app.task import bp as task_bp

    app.register_blueprint(task_bp)

    if not app.debug and not os.path.exists('logs'):
        os.mkdir('logs')
    if not app.debug:
        file_handler = RotatingFileHandler('logs/kursoagregator.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)
    return app


from app import models, admin, task
