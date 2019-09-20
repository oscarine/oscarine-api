from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response


'''
The 'errors/404.html' and 'errors/500.html' are not
created yet as we will be focusing on API friendly
errors rather then web based or browser based errors.
With this approach we are not assuming that API client
will be the browser instead we are taking the general
approach in which anyone can be a client be it android,
ios app or some browser based single page application.
'''


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500


@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(403)
def internal_error(error):
    if wants_json_response():
        return api_error_response(403, message="You aren't allowed to edit this source")
    return render_template('errors/403.html'), 403
