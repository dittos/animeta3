from animeta import db
from animeta.models import History, Record

def _base_query():
    return (History.query.filter(History.comment != '')
                .order_by(History.id.desc()))

def get_recent_posts(work=None, filter_noise=False):
    q = _base_query()
    if work:
        q = q.filter_by(work=work)
    if filter_noise:
        # 두 명 이상이 기록한 작품만 포함
        stats = (db.session.query(Record.work_id, db.func.count().label('score'))
                           .group_by(Record.work_id)
                           .subquery())
        q = (q.join(stats, History.work_id == stats.c.work_id)
                .filter(stats.c.score >= 2))
    return q
