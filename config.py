import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB') or 'postgresql://kursoagregator_rikp_user:Xw88Uf2bXVrrZ1oQLNPDFUdkqnbojIqe@dpg-cnnffp779t8c739i33fg-a.frankfurt-postgres.render.com/kursoagregator_rikp'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zxczxc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COURSE_PER_PAGE = 26
    TECHNOLOGY_PER_PAGE = 9
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or 'simple'
    SQLALCHEMY_ECHO = False
    CACHE_REDIS_HOST = os.environ.get('CACHE_HOST')
    ADMINS = ['mrpostik@gmail.com']
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300
