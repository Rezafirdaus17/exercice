from datetime import datetime, timedelta

from app import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(13), nullable=True)
    date_of_birthday = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, name, email, phone_number, date_of_birthday):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birthday = datetime.strptime(date_of_birthday, '%d %m %Y')

    def to_json(self):
        return {
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'date_of_birthday': self.date_of_birthday.strftime("%d %m %Y")
        }

    def __repr__(self):
        return 'User: %r' % self.name


class PromoCodeModel(db.Model):
    __tablename__ = 'event_promo_code'

    id = db.Column(db.Integer, primary_key=True)
    promo_code = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float(10), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, promo_code, description, user_id, amount):
        self.promo_code = promo_code
        self.description = description
        self.user_id = user_id
        self.amount = amount
        self.start_date = datetime.now()
        self.end_date = datetime.now() + timedelta(days=1)

    def to_json(self):
        return {
            'promo_code': self.promo_code,
            'description': self.description,
            'amount': self.amount,
            'end_date': self.end_date.strftime("%d %m %Y %H:%M"),
        }

    def __repr__(self):
        return 'Promo: %r' % self.promo_code
