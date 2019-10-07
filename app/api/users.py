from app.api import bp
from flask import jsonify, url_for, request
from app.models import User
from app import db
from app.api.errors import bad_request, error_response
from flask_jwt_extended import jwt_required, get_jwt_identity,\
    create_access_token


@bp.route('/users/<int:id>', methods=['GET'])
@jwt_required
def get_user(id):
    user = User.query.get_or_404(id)
    if user.username == get_jwt_identity():
        return jsonify(user.to_dict())
    return error_response(401)


@bp.route('/users', methods=['GET'])
def get_users():
    pass


@bp.route('/users', methods=['POST'])
def create_user():
    # registering new users
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
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/login', methods=['POST'])
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


@bp.route('/users', methods=['PUT'])
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
