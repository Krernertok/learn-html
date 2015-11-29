from flask import jsonify, request
from . import api
from .errors import bad_request
from ..tagnames.tagnames import get_definition as get_def
from ..tagnames.tagnames import get_remaining_tags as get_tags

@api.route('/definition')
def get_definition():
    tag_name = request.args.get('tagname')
    if tag_name is None:
        return bad_request('Tag name not included in request.')
    definition = get_def(tag_name)
    return jsonify({"definition": definition})

@api.route('/remaining_tags')
def get_remaining_tags():
    answered_tag_names = request.args.get('alreadyAnswered')
    if answered_tag_names is None:
        return bad_request('Tag names not included in request.')
    return jsonify(get_tags(answered_tag_names))