from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import MetaData

from config import Config

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

migrate = Migrate()
login_manager = LoginManager()
admin_app = Admin(name='KursoAgregator', template_mode='bootstrap3')
db = SQLAlchemy(metadata=MetaData(naming_convention=convention))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    db.init_app(app)
    admin_app.init_app(app)
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.review import bp as review_bp

    app.register_blueprint(review_bp)

    return app


from app import models, admin
