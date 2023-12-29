import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zxczxc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COURSE_PER_PAGE = 26
    CACHE_TYPE = 'RedisCache'  # Flask-Caching related configs
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300
