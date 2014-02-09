from animeta import models, db

def get_work(title):
    return models.Work.query.filter_by(title=title).first()

def get_episodes(work):
    q = (db.session.query(models.History.status)
            .filter(
                models.History.comment != '',
                models.History.work == work
            )
            .order_by(models.History.status)
            .distinct())
    result = []
    for status, in q:
        try:
            episode = int(status)
        except ValueError:
            continue
        result.append(episode)
    return sorted(result)
