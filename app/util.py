import re
from datetime import datetime

import pytz
from flask import jsonify


def running_sender_email():
    from flask_mail import Message
    from app import app, db, mail
    from app.models import EmailModel

    print("Run Schedule")

    with app.app_context():
        get_all_data = EmailModel.query.filter_by(has_sent=False).filter(
            EmailModel.sent_at < show_datetime_singapore()
        ).all()

        for x in get_all_data:
            msg = Message(
                subject=x.email_subject,
                sender="no-reply@demo.com",
                recipients=[x.email],
                body=x.email_content
            )
            mail.send(msg)
            email = EmailModel.query.get(x.id)
            email.has_sent = True
            db.session.commit()

        print("Success Run Schedule")


def show_datetime_singapore():
    singapore = datetime.now(pytz.timezone('Asia/Singapore'))

    return singapore.replace(microsecond=0, tzinfo=None)


def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    return True if re.fullmatch(regex, email) else False


def response_invalid_email():
    return jsonify({
            'status': '400',
            'res': 'Bad request',
            'msg': 'Invalid email format. Please enter a valid email address'
        }), 400


def response_data_exists():
    return jsonify({
        'status': '400',
        'res': 'Bad request',
        'msg': "Email has been used.",
    }), 400


def response_invalid_timestamp():
    return jsonify({
        'status': '400',
        'res': 'Bad request',
        'msg': "Timestamp must be after date time now.",
    }), 400
