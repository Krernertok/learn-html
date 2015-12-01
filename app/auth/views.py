from . import auth
from flask import render_template, redirect, current_app, flash, request
from flask import url_for
from .forms import LoginForm
from ..models import User
from flask.ext.login import login_user


@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_on(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("You have been logged in.")
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('/auth/login.html', form=form)