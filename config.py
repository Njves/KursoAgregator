import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://njves:ViX8tAxl4Gn67J8kplD9uA8gAC451IM2@dpg-clpv7phjvg7s73e1e8m0-a.frankfurt-postgres.render.com/kursoagregator'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zxczxc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COURSE_PER_PAGE = 25
