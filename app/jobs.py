import random
import string
from datetime import datetime, date

from sqlalchemy import extract


def running_sender_coupon():
    from flask_mail import Message
    from app import app, db, mail
    from app.models import UserModel, PromoCodeModel

    print("Run Sender Coupon Schedule")

    with app.app_context():
        today = date.today()

        get_all_data = UserModel.query.filter(
            extract('month', UserModel.date_of_birthday) == today.month
        ).filter(extract('day', UserModel.date_of_birthday) == today.day).all()

        for x in get_all_data:
            ran = ''.join(random.choices(string.ascii_uppercase, k=3))

            get_age = today.year - x.date_of_birthday.year - (
                    (today.month, today.day) < (x.date_of_birthday.month, x.date_of_birthday.day)
            )

            promo_code = "BIRTHDAY" + ran + str(get_age)
            desc = "Happy Birthday, we send coupon birthday to celebrate your birthday"
            amount = get_age * 1000

            data = PromoCodeModel(str(promo_code), desc, x.id, amount)
            db.session.add(data)
            db.session.commit()

            coupon_data = data.to_json()
            body = (
                    desc + " with coupon code promo " + coupon_data["promo_code"] + " You can use this coupon until " +
                    coupon_data["end_date"] + " With amount " + str(coupon_data["amount"]) + " Happy Shopping !!!"
            )

            msg = Message(
                subject="Happy Birthday From Zaa Company",
                sender="no-reply@demo.com",
                recipients=[x.email],
                body=body
            )
            mail.send(msg)

    print("Success Run Coupon Schedule")


def running_check_coupon():
    from app import app, db
    from app.models import PromoCodeModel

    with app.app_context():
        get_all_data = PromoCodeModel.query.filter_by(is_valid=True).filter(
            PromoCodeModel.end_date < datetime.now()
        ).all()

        for y in get_all_data:
            coupon = PromoCodeModel.query.get(y.id)
            coupon.is_valid = False
            db.session.commit()

    print("Success Run Coupon Schedule")
