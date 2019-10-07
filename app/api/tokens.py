from flask import g
from app import db
from app.api import bp
from app.api.auth import token_auth


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
