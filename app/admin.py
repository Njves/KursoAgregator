from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, AnonymousUserMixin

from app import admin_app, db
from app.models import User, Review, Course, School, Technology


class SecurityModelView(ModelView):
    column_display_pk = True
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'admin'


admin_app.add_view(SecurityModelView(User, db.session, endpoint='user'))
admin_app.add_view(SecurityModelView(Review, db.session, endpoint='reviews'))
admin_app.add_view(SecurityModelView(Course, db.session, endpoint='courses'))
admin_app.add_view(SecurityModelView(School, db.session, endpoint='schools'))
admin_app.add_view(SecurityModelView(Technology, db.session, endpoint='technologies'))
