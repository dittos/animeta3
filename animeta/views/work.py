import flask
from animeta import apis

bp = flask.Blueprint('work', __name__)

@bp.app_template_filter()
def work_url(work, endpoint='detail', **kwargs):
    return flask.url_for('work.' + endpoint, title=work.title, **kwargs)

@bp.route('/<title>/')
def detail(title):
    work = apis.work.get_work(title)
    return flask.render_template('work/detail.html',
        work=work,
        posts=apis.post.get_recent_posts(work).limit(6),
    )
