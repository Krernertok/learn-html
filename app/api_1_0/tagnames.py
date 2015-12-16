from flask import jsonify, request, session
from flask.ext.login import current_user
from . import api
from .. import db
from .errors import bad_request
from ..models import Tag, Session, User


@api.route('/definition')
def get_definition():
    tag_name = request.args.get('tagname')
    if tag_name is None:
        return bad_request('Tag name not included in request.')
    s_id = session.get('session_id')
    quiz_session = Session.query.filter_by(session_id=s_id).first()
    if quiz_session is None and current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        quiz_session = Session(session_id=s_id, user_id=user.id)
        db.session.add(quiz_session)
    definition = Tag.get_definition(name=tag_name)
    if s_id and definition:
        tag = Tag.query.filter_by(name=tag_name).first()
        quiz_session.right_answers.append(tag)
        db.session.add(quiz_session)
    return jsonify({"definition": definition})
    

@api.route('/remaining_tags')
def get_remaining_tags():
    answered_tag_names = request.args.getlist('answered')
    if answered_tag_names is None:
        return bad_request('Tag names not included in request.')
    return jsonify(Tag.get_remaining_tags(answered_tag_names))