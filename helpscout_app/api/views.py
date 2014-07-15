import json
from flask import request, jsonify, current_app as app
from mosql.query import select, left_join
from mosql.db import one_to_dict
from mosql.util import identifier
from ..decorators import signed_request
from ..core import db
from . import api


@api.route('/get-user/', methods=['POST'])
@signed_request
def get_user():
    """Retreives a single user from a Database, and render it using a HTML template"""
    try:
        data = json.loads(request.data)
    except ValueError:
        return '', 400
    else:
        email = data['customer']['email']

    # For more complex queries, consider moving queries to a separate module
    with db as cur:
        cur.execute(select('auth_user', {'email': email}, select=('username')))
        try:
            user = one_to_dict(cur)
        except TypeError:
            return '', 404

    template = app.jinja_env.get_template('api/helpscout.html')
    return jsonify({'html': template.render(user)})
