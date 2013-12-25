from animeta.models import History

def _base_query():
    return (History.query.filter(History.comment != '')
                .order_by(History.id.desc()))

def get_recent_posts(work=None):
    q = _base_query()
    if work:
        q = q.filter_by(work=work)
    return q
