from animeta import models, db

def get_user(username):
    return models.User.query.filter_by(username=username).first()
