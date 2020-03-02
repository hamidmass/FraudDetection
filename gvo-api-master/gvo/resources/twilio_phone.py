from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required


from gvo.app import twilio
from gvo.parsers.phone_parser import PhoneParser
from gvo.parsers.search_parser import SearchParser
from gvo.controllers.phone_controller import PhoneController
from gvo.validators.user_validator import UserValidator


twilio_phone = Blueprint('twilio_phone', __name__)


@twilio_phone.route("/phone")
@jwt_required
def search_phones():
    data = SearchParser(request)
    UserValidator.validate_user()
    phones = PhoneController.search_phones(data, twilio)
    return jsonify({"Phones": phones}), '200'


@twilio_phone.route("/phone", methods=["POST"])
@jwt_required
def buy_phone():
    data = PhoneParser(request)
    user = UserValidator.validate_user()
    PhoneController.buy_phone(user, data, twilio)
    return "", '204'


@twilio_phone.route("/phone", methods=["PUT"])
@jwt_required
def update_phone():
    data = PhoneParser(request)
    PhoneController.update_phone(data, twilio)
    return "", '204'


@twilio_phone.route("/phone", methods=["DELETE"])
@jwt_required
def delete_phone():
    data = PhoneParser(request)
    PhoneController.delete_phone(data, twilio)
    return "", '204'

