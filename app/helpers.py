import re

from flask import jsonify


def validation_email(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    return True if re.fullmatch(regex, email) else False


def response_created_request(data):
    return jsonify({"status": 201, "msg": "Success Create Data", "results": data}), 201


def response_bad_request(msg):
    return jsonify({'status': '400', 'res': 'Bad request', 'msg': msg}), 400
