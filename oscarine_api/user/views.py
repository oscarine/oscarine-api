# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, request, jsonify, url_for
from oscarine_api.user.models import User
from oscarine_api.errors import bad_request, error_response
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, decode_token
from oscarine_api.extensions import db

blueprint = Blueprint("user", __name__, url_prefix="/api/v1", static_folder="../static")


@blueprint.route("/users/<int:id>", methods=['GET'])
@jwt_required
def get_user(id):
    user = User.query.get_or_404(id)
    if user.username == get_jwt_identity():
        return jsonify(user.to_dict())
    return error_response(401)


@blueprint.route("/users", methods=['POST'])
def create_user():
    """registering new users."""
    data = request.get_json() or {}
    print(request)
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    user.verify_email()
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('user.get_user', id=user.id)
    return response

@blueprint.route("/confirm_email/<mail_token>", methods=['GET'])
def confirm_email(mail_token):
    """verify email via jwt"""
    current_user = decode_token(mail_token)
    user = User.query.filter_by(username=current_user['identity']).first_or_404()
    user.email_verified()
    db.session.commit()
    response = jsonify({
                        "success": "true",
                        "message": "your email has been successfully confirmed"
                        })
    response.status_code = 201
    response.headers['Location'] = url_for('user.get_user', id=user.id)
    return response

@blueprint.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return bad_request('Missing JSON in request')
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return bad_request('Missing username parameter')
    if not password:
        return bad_request('Missing password parameter')
    user = User.query.filter_by(username=username).first_or_404()
    password_is_correct = user.check_password(password)
    if not (user and password_is_correct):
        return error_response(401, 'Bad username or password')
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@blueprint.route('/users', methods=['PUT'])
@jwt_required
def update_user():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first_or_404()
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
