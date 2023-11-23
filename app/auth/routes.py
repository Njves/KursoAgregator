import flask
from flask import render_template, request, redirect, url_for
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
        if request.form.get('type') == 'register':
            reg_login, reg_email, reg_password = request.form.get('reg_login'), \
                request.form.get('reg_email'), request.form.get('reg_password')
            user = User(username=reg_login, email=reg_email)
            user.set_password(reg_password)
            db.session.add(user)
            db.session.commit()
        if request.form.get('type') == 'login':
            user = User.query.filter_by(email=request.form.get('email')).one()
            if user is None:
                redirect(url_for('auth.login'))
                return
            user.check_password(str(request.form.get('password')))
            if user.check_password(request.form.get('password')):
                login_user(user, remember=True)
                next = flask.request.args.get('next')
                return flask.redirect(next or flask.url_for('main.index'))
        redirect(url_for('auth.login'))
    return render_template('auth/login.html')


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
