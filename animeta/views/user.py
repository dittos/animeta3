import flask
from animeta import apis, models

bp = flask.Blueprint('user', __name__)

@bp.app_template_filter()
def user_url(user, endpoint='detail', **kwargs):
    return flask.url_for('user.' + endpoint, username=user.username, **kwargs)

@bp.app_template_filter()
def record_url(record, endpoint='detail', **kwargs):
    return flask.url_for('user.record_' + endpoint,
        username=record.user.username, id=record.id, **kwargs)

@bp.app_template_filter()
def format_status(record):
    # TODO: move to appropriate module
    status = record.status.strip()
    status_type = models.StatusType.TEXTS[record.status_type]
    if not status:
        return status_type

    if status[-1].isdigit():
        status += '화'
    if record.status_type != models.StatusType.WATCHING:
        status += ' (' + status_type + ')'
    return status

@bp.route('/')
def detail(username):
    user = apis.user.get_user(username)
    records = apis.record.get_records(user)
    return flask.render_template('user/detail.html',
        user=user,
        records=records,
    )

@bp.route('/<id>/')
def record_detail(username, id):
    user = apis.user.get_user(username)
    record = apis.record.get_record(id)
    if record.user != user:
        flask.abort(404)
    return flask.render_template('user/record_detail.html',
        user=user,
        record=record,
        history_list=apis.record.get_history(record),
    )
