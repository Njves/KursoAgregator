import flask
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.emal import send_password_reset_email
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
            return redirect(url_for('auth.login'))
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

@bp.route('/forgot')
def forgot_password():
    if not current_user.is_authenticated:
        return render_template('auth/forgot.html')
    return flask.abort(403)

@bp.route('/forgot', methods=['POST'])
def forgot_send():
    if email := request.form.get('email'):
        flash('На вашу почту отправленно сообщение с инструкциями по восстановлению пароля')
        send_password_reset_email(User.query.filter_by(email=email).first())
    return redirect(url_for('auth.forgot_password'))

@bp.route('/reset/<token>')
def reset_password(token):
    if 'blacklist' in flask.session:
        if flask.session['blacklist'] == token:
            return flask.abort(403)
    user = User.verify_reset_password_token(token)
    if not user:
        return flask.abort(403)
    return render_template('auth/reset.html', token=token)

@bp.route('/reset/<token>', methods=['POST'])
def update_password(token):
    user = User.verify_reset_password_token(token)
    if password := request.form.get('password'):
        flask.session['blacklist'] = token
        user.set_password(password)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return redirect(url_for('auth.reset_password', token=token))

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
