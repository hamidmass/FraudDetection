from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from gvo.controllers.phone_controller import PhoneController
from gvo.validators.user_validator import UserValidator


phone_number = Blueprint('phone_number_getter', __name__)


@phone_number.route('/user/phone')
@jwt_required
def get_phone_numbers():
    user = UserValidator.validate_user()
    phone_type = request.args.get('phone_type')
    phones = PhoneController.get_phone_numbers(user, phone_type)
    return jsonify({"phones": phones}), 200
