import datetime
import flask
from babel.dates import format_timedelta
from animeta import db, models, apis

def init_app(app):
    from animeta.views import chart
    app.register_blueprint(chart.bp, url_prefix='/charts')

    # The trailing parenthesises make the filter name
    # same with the function name (`static`).
    @app.template_filter()
    def static(filename):
        # We don't use `url_for('static')` directly.
        # It's hard to override the default URL generation.
        # Sometimes you will need to change the host to CDN, for example.
        # TODO: consider static files per blueprint.
        return flask.url_for('static', filename=filename)

    @app.template_filter()
    def timesince(dt):
        delta = datetime.datetime.now(datetime.timezone.utc) - dt
        return format_timedelta(delta, locale='ko')

    @app.route('/')
    def index():
        work_chart = apis.chart.get_work_chart(apis.chart.get_date_range('weekly'), limit=10)
        return flask.render_template('index.html',
            work_chart=work_chart,
            timeline=apis.post.get_recent_posts().limit(6),
        )
