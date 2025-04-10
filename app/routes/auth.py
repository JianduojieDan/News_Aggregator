from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app import db
from app.models.models import User
from app.routes.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('news.index')

        flash('You have been logged in successfully!', 'success')
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('news.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # 在实际应用中，这里应该发送重置密码的邮件
            # 为了简化，我们只显示一个成功消息
            flash('Check your email for the instructions to reset your password', 'info')
        else:
            flash('Email address not found', 'warning')

        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))

    # 在实际应用中，这里应该验证token并获取用户
    # 为了简化，我们只显示重置密码表单
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # 在实际应用中，这里应该更新用户密码
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', title='Reset Password', form=form)
