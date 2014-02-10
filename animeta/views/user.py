import flask
from animeta import apis

bp = flask.Blueprint('user', __name__)

@bp.app_template_filter()
def user_url(user, endpoint='detail', **kwargs):
    return flask.url_for('user.' + endpoint, username=user.username, **kwargs)

@bp.route('/<username>/')
def detail(username):
    return username
