from flask_admin.contrib.sqla import ModelView
from app import admin_app, db
from app.models import User, Review, Course, School, Technology


class SecurityModelView(ModelView):
    def is_accessible(self):
        # TODO: Добавить проверку
        return True


admin_app.add_view(ModelView(User, db.session, endpoint='accounts'))
admin_app.add_view(ModelView(Review, db.session, endpoint='mems'))
admin_app.add_view(ModelView(Course, db.session))
admin_app.add_view(ModelView(School, db.session))
admin_app.add_view(ModelView(Technology, db.session, endpoint='technology'))
