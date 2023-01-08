from datetime import datetime

from flask import jsonify, request, abort

from app import app, db
from app.helpers import validation_email, response_bad_request
from app.models import UserModel, PromoCodeModel


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/accounts", methods=['POST'])
def save_accounts():
    data = request.get_json()

    for x in ["name", "email", "date_of_birthday"]:
        if x not in data:
            return response_bad_request("fields " + x + " must be include")

    if not validation_email(data['email']):
        return response_bad_request("Email Not Valid")

    check = UserModel.query.filter_by(email=data["email"]).first()
    if check:
        return response_bad_request("Email Has Been Registered")

    db.session.add(UserModel(
        data["name"],
        data["email"],
        data.get("phone_number", ""),
        data["date_of_birthday"],
    ))
    db.session.commit()
    return jsonify({"status": 201, "msg": "Success Create Data", "results": data}), 201


@app.route("/accounts/<int:id>", methods=['GET'])
def get_account(id):
    data = UserModel.query.get(id)
    if data is None:
        abort(404)

    coupon = PromoCodeModel.query.filter_by(user_id=data.id).filter_by(is_valid=True).filter(
        PromoCodeModel.end_date >= datetime.now()
    ).all()

    users = data.to_json()
    users['coupon'] = [coupons.to_json() for coupons in coupon]

    return jsonify(users)
