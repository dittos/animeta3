from animeta import models

def get_records(user):
    return user.records.order_by(models.Record.updated_at.desc().nullslast())

def get_record(id):
    return models.Record.query.get(id)

def get_history(record):
    return (models.History.query
        .filter_by(user=record.user, work=record.work)
        .order_by(models.History.id.desc()))
