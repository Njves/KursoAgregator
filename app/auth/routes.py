import flask
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app import db, login_manager
from app.auth import bp
from app.models import User



@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Auth page
    """
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user is None:
            flash('Пользователь не найден')
            redirect(url_for('auth.login'))
            return
        user.check_password(str(request.form.get('password')))
        if user.check_password(request.form.get('password')):
            login_user(user, remember=True)
            next = flask.request.args.get('next')
            return flask.redirect(next or flask.url_for('main.index'))
        flash('Пароль неправильный')
        return redirect('auth.login')
    return render_template('auth/login.html')


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        reg_login, reg_password = request.form.get('username'), request.form.get('password')
        if len(reg_login) > 128 or len(reg_password) > 128:
            flash('Слишком длинные значения')
            return redirect(request.referrer)
        user = User(username=reg_login)
        user.set_password(reg_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        next = flask.request.args.get('next')
        return flask.redirect(next or flask.url_for('main.index'))
    return render_template('auth/register.html')


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
