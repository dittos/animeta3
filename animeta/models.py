import datetime
import pytz
from sqlalchemy.ext.associationproxy import association_proxy
from animeta import db

class User(db.Model):
    __tablename__ = 'auth_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(30), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __str__(self):
        return self.username

class Work(db.Model):
    __tablename__ = 'work_work'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('title', db.Unicode(100), nullable=False, index=True)

    title_mappings = db.relationship('TitleMapping', backref=db.backref('work'))
    titles = association_proxy('title_mappings', 'title')

    def __str__(self):
        return self.title

class TitleMapping(db.Model):
    __tablename__ = 'work_titlemapping'
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.ForeignKey(Work.id), nullable=False)
    title = db.Column(db.Unicode(100), nullable=False)
    key = db.Column(db.Unicode(100), nullable=False)

class StatusType(db.TypeDecorator):
    impl = db.Integer

    NONE = ''
    FINISHED = 'finished'
    WATCHING = 'watching'
    SUSPENDED = 'suspended'
    INTERESTED = 'interested'
    table = (FINISHED, WATCHING, SUSPENDED, INTERESTED)
    TEXTS = {
        FINISHED: '완료',
        WATCHING: '보는 중',
        SUSPENDED: '중단',
        INTERESTED: '볼 예정',
    }

    def process_bind_param(self, value, dialect):
        if value == self.NONE:
            return -1
        return self.table.index(value)

    def process_result_value(self, value, dialect):
        if value == -1:
            return self.NONE
        return self.table[value]

class History(db.Model):
    __tablename__ = 'record_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id), nullable=False)
    work_id = db.Column(db.ForeignKey(Work.id), nullable=False)
    status_type = db.Column(StatusType, nullable=False, default=StatusType.NONE)
    status = db.Column(db.Unicode(30))
    updated_at = db.Column(db.DateTime(timezone=True))
    comment = db.Column(db.UnicodeText, nullable=False)

    user = db.relationship(User, backref=db.backref('history', lazy='dynamic'))
    work = db.relationship(Work, backref=db.backref('history', lazy='dynamic'))

    def __init__(self, **kwargs):
        self.updated_at = datetime.datetime.now(pytz.utc)
        super(Update, self).__init__(**kwargs)

    @property
    def progress(self):
        progress = (self.status or '').strip()
        if progress:
            if progress.endswith(tuple('0123456789')):
                progress += '화'
        else:
            progress = StatusType.TEXTS[self.status_type]
        return progress

class Record(db.Model):
    __tablename__ = 'record_record'
    __table_args__ = (db.UniqueConstraint('user_id', 'work_id'), )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey(Work.id), nullable=False)
    title = db.Column(db.Unicode(100), nullable=False)
    status_type = db.Column(StatusType, nullable=False, default=StatusType.WATCHING)
    status = db.Column(db.Unicode(30))
    updated_at = db.Column(db.DateTime(timezone=True))

    user = db.relationship(User, backref=db.backref('records', lazy='dynamic'))
    work = db.relationship(Work, backref=db.backref('records', lazy='dynamic'))
