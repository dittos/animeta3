import flask
from animeta import db, models

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
