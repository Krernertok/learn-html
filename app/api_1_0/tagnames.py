from flask import jsonify, request, session
from . import api
from .. import db
from .errors import bad_request
from ..models import Tag, Session


@api.route('/definition')
def get_definition():
    tag_name = request.args.get('tagname')
    if tag_name is None:
        return bad_request('Tag name not included in request.')
    definition = Tag.get_definition(name=tag_name)
    s_id = session.get('session_id')
    if s_id and definition:
        quiz_session = Session.query.filter_by(session_id=s_id).first()
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