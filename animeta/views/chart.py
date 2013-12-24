import flask
from animeta.apis import chart as api

bp = flask.Blueprint('chart', __name__)

@bp.route('/works/<any(overall,weekly,monthly):range>/', endpoint='work')
def work_chart(range):
    date_range = api.get_date_range(range)
    chart = api.get_work_chart(date_range)
    return flask.render_template('chart/work.html', range=range, date_range=date_range, chart=chart)

@bp.route('/users/<any(overall,weekly,monthly):range>/', endpoint='user')
def user_chart(range):
    date_range = api.get_date_range(range)
    chart = api.get_user_chart(date_range)
    return flask.render_template('chart/user.html', range=range, date_range=date_range, chart=chart)
