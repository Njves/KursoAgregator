from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import User, Technology
from app.user import bp


@bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile_view(user_id):
    user = User.query.get_or_404(user_id)
    subscribed_technologies = [technology.id for technology in user.subscribed_technologies]
    technologies = Technology.query.all()
    return render_template('user/main.html', user=user, subscribed_technologies=subscribed_technologies, technologies=technologies)

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

@bp.route('/<int:user_id>/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        selected_technologies = request.form.getlist('technologies[]')
        user.subscribed_technologies = []
        for technology_id in selected_technologies:
            technology = Technology.query.get_or_404(technology_id)
            user.subscribed_technologies.append(technology)
        db.session.commit()
    return redirect(url_for('user_bp.profile_view', user_id=user_id))