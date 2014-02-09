from animeta import models

def get_work(title):
    return models.Work.query.filter_by(title=title).first()
