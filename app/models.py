from datetime import datetime

from app import db
from app.util import show_datetime_singapore


class EmailModel(db.Model):
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True, nullable=False)
    email_subject = db.Column(db.String(500), nullable=False)
    email_content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=show_datetime_singapore())
    sent_at = db.Column(db.DateTime)
    has_sent = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, event_id, email, email_subject, email_content, timestamp):
        self.event_id = event_id
        self.email = email
        self.email_subject = email_subject
        self.email_content = email_content
        self.sent_at = datetime.strptime(timestamp, '%d %b %Y %H:%M')

    def __repr__(self):
        return '<Email %r>' % self.email
