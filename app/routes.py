from flask import render_template
from datetime import datetime
from flask_login import current_user
from app import app, db


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Documentation')


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
