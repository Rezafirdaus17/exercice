from datetime import datetime, timedelta

from flask import jsonify, request

from app import app, db
from app.models import EmailModel
from app.util import (
    isValid,
    response_invalid_email,
    response_data_exists,
    show_datetime_singapore,
    response_invalid_timestamp
)


@app.route("/save_emails", methods=['POST'])
def save_emails():
    data = request.get_json()
    fields = ["event_id", "email", "email_subject", "email_content", "timestamp"]

    for x in fields:
        if x not in data:
            return jsonify({
                'status': '400',
                'res': 'Bad request',
                'msg': "fields " + x + " must be include",
            }), 400

    if not isValid(data['email']):
        return response_invalid_email()

    check = EmailModel.query.filter_by(email=data["email"]).first()
    if check:
        return response_data_exists()

    data_date = datetime.strptime(data["timestamp"], '%d %b %Y %H:%M')
    singapore = data_date + timedelta(hours=1)

    if singapore <= show_datetime_singapore():
        return response_invalid_timestamp()

    db.session.add(EmailModel(
        data["event_id"],
        data["email"],
        data["email_subject"],
        data["email_content"],
        data["timestamp"],
    ))
    db.session.commit()
    return jsonify({"status": 201, "msg": "Success Create Data", "results": data}), 201
