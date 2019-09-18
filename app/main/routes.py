from flask import render_template
from datetime import datetime
from flask_login import current_user
from app import db
from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    return render_temdsewdewplate('index.html', title='Documentation')


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()dewdewdewddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        db.session.commit()
