from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import User
from app.user import bp


@bp.route('/profile/<int:user_id>')
@login_required
def profile_view(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user/main.html', user=user)

@bp.route('/user/<int:user_id>/password/update', methods=['POST'])
@login_required
def update_password_profile(user_id):
    form = request.form
    password = form.get('password')
    password_repeat = form.get('password_repeat')
    if password != password_repeat:
        return redirect(url_for('user_bp.profile_view', user_id=user_id))
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return redirect(url_for('user_bp.profile_view', user_id=user_id))
    if len(password) < 6:
        return redirect(url_for('user_bp.profile_view', user_id=user_id))
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash('Пароль успешно обновлен')
    return redirect(url_for('user_bp.profile_view', user_id=user_id))

