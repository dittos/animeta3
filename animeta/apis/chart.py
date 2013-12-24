import datetime
from animeta import db, models

OVERALL_RANGE = (datetime.date.min, datetime.date.max)

def get_date_range(range_str):
    if range_str == 'overall':
        return OVERALL_RANGE
    elif range_str == 'weekly':
        return last_week_range()
    elif range_str == 'monthly':
        return last_month_range()
    else:
        raise ValueError

def last_month_range():
    today = datetime.date.today()
    y, m = today.year, today.month
    # 지난달을 구한다
    if m == 1:
        y, m = y - 1, 12
    else:
        m -= 1
    # 지난달 = y년 m월 1일 <= t < 이번달 1일
    start = datetime.date(y, m, 1)
    end = datetime.date(today.year, today.month, 1)
    return (start, end)

def last_week_range():
    today = datetime.date.today()
    # datetime 모듈은 ISO weekday system을 사용하므로 월요일이 1, 일요일이 7
    # 일요일을 0, 토요일을 6으로 맞추기 위해 변환한다.
    weekday = today.isoweekday()
    if weekday == 7: weekday = 0
    sunday = today - datetime.timedelta(days=weekday)
    # 지난주 = 이번주 일요일 - 7일 <= t < 이번주 일요일
    start = sunday - datetime.timedelta(days=7)
    end = sunday
    return (start, end)

class ChartItem(object):
    def __init__(self, obj, score, rank, maxscore):
        self.obj = obj
        self.score = score
        self.score_percent = (score / maxscore) * 100
        self.rank = rank
        self.diff = None

def ranked(it):
    rank = 0
    prev = -1
    ptr = 1
    max = None

    for obj, score in it:
        if prev != score:
            rank = ptr
        prev = score
        if max is None:
            max = score
        ptr += 1
        yield ChartItem(obj, score, rank, max)

def compare(cur, prev):
    prev_ranks = {}
    for item in prev:
        prev_ranks[item.obj] = item.rank
    for item in cur:
        if item.obj not in prev_ranks:
            item.diff = None
        else:
            item.diff = prev_ranks[item.obj] - item.rank
        yield item

def _get_chart(model, group_field, score_field, date_range):
    start_date, end_date = date_range
    # TODO: timezone?
    stats = (db.session.query(group_field.label('group'), score_field.label('score'))
                       .group_by(group_field)
                       .filter(models.History.updated_at >= start_date)
                       .filter(models.History.updated_at < end_date)
                       .subquery())
    q = (db.session.query(model, stats.c.score)
                   .join(stats, model.id == stats.c.group)
                   .filter(stats.c.score > 1)
                   .order_by(stats.c.score.desc()))
    return ranked(q)

def get_chart(model, group_field, score_field, date_range):
    result = _get_chart(model, group_field, score_field, date_range)
    if date_range != OVERALL_RANGE:
        s, e = date_range
        delta = e - s
        prev_chart = _get_chart(
            model, group_field, score_field,
            (s - delta, e - delta)
        )
        result = compare(result, prev_chart)
    return result

def get_work_chart(date_range):
    return get_chart(
        models.Work,
        models.History.work_id,
        db.func.count(models.History.user_id.distinct()),
        date_range
    )

def get_user_chart(date_range):
    return get_chart(
        models.User,
        models.History.user_id,
        db.func.count(),
        date_range
    )
