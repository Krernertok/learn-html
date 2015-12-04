from . import auth
from .. import db
from flask import render_template, redirect, current_app, flash, request
from flask import url_for
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from .forms import RequestPasswordResetForm, ResetPasswordForm, ChangeEmailForm
from ..models import User
from flask.ext.login import login_user, login_required, current_user
from flask.ext.login import logout_user
from ..email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
            'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('Your account has been confirmed.')
    else:
        flash('Your confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email('auth/email/confirm', 'Confirm Your Account', user, token=token)
    flash('A new confirmation email has been sent to you.')
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("You have been logged in.")
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('/auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You\'ve been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been changed.')
            return redirect(url_for('main.index'))
        else:
            flash('Incorrect password')
    return render_template('auth/change-password.html', form=form)


@auth.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                'auth/email/reset-password',
                user=user, token=token,
                next=request.args.get('next'))
            flash('An email with instruction to reset your password has'
            'been sent to your email address.')
            return redirect(url_for('auth.login'))
        else:
            flash('Email is not registered.')
    return render_template('auth/reset-password.html', form=form)    


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Email address doesn\'t exist.')
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been reset.')
            return redirect(url_for('auth.login'))
        else:
            flash('Your token is invalid or has expired. '
                  'Please request another reset.')
    return render_template('auth/reset-password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def request_email_change():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_token(new_email)
            send_email(new_email, 'Confirm your email address',
                'auth/email/change-email',
                user=current_user, token=token)
            flash('An email with instructions on how to verify your '
                  'new account has been sent to the provided address.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template('auth/change-email.html', form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email has been changed.')
    else:
        flash('Something went wrong. Please try to change your email again.')
    return redirect(url_for('main.index'))