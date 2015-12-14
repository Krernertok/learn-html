from uuid import uuid4
from flask import render_template, session, request, redirect, url_for
from flask import current_app
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from ..models import Session, User, Tag


@main.route('/')
def index():
    if request.args.get('guest') == 'true':
        session['guest'] = True
    if session.get('guest') != True:
        return redirect(url_for('auth.login'))
    if current_user.is_authenticated:
        session_id = str(uuid4())
        session['session_id'] = session_id
    tag_count = Tag.query.count()
    return render_template('index.html', tag_count=tag_count)


@main.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first()
    sessions = Session.query.filter_by(
        user_id=user.id).order_by(Session.session_start.desc())
    count = Tag.query.count()
    return render_template('profile.html', sessions=sessions, count=count)