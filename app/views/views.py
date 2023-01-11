import app.setting as app_settings

from datetime import datetime

from flask import jsonify, request, abort
from flask.views import MethodView

from app import db
from app.helpers import validation_email, response_bad_request, response_created_request
from app.models.models import UserModel, PromoCodeModel


class HomeAPIView(MethodView):
    def get(self):
        return jsonify({'message': 'Hello, World!'})


class CreateAccountAPIView(MethodView):
    def post(self):
        data = request.get_json()

        for x in app_settings.REQUIRED_FIELDS:
            if x not in data:
                return response_bad_request(app_settings.MSG_FIELD_MUST_BE_INCLUDE % x)

        if not validation_email(data['email']):
            return response_bad_request(app_settings.MSG_EMAIL_INVALID)

        check = UserModel.query.filter_by(email=data["email"]).first()
        if check:
            return response_bad_request(app_settings.MSG_EMAIL_DUPLICATED)

        db.session.add(UserModel(
            data["name"],
            data["email"],
            data.get("phone_number", ""),
            data["date_of_birthday"],
        ))
        db.session.commit()

        return response_created_request(data)


class GetAccountAPIView(MethodView):
    def get(self, id):
        data = UserModel.query.get(id)
        if data is None:
            abort(404)

        coupon = PromoCodeModel.query.filter_by(user_id=data.id).filter_by(is_valid=True).filter(
            PromoCodeModel.end_date >= datetime.now()
        ).all()

        users = data.to_json()
        users['coupon'] = [coupons.to_json() for coupons in coupon]

        return jsonify(users)
