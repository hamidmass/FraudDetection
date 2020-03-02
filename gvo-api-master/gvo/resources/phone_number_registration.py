import logging
from flask import request, jsonify
from sqlalchemy_utils import PhoneNumber
from gvo.app import db
from gvo.models import phone_number
from gvo.models.phone_number import PhoneNumber
from flask_jwt_extended import jwt_required
from flask import Blueprint

phone_number_registration_route = Blueprint('phone_number', __name__)


@phone_number_registration_route.route('/phone_number', methods=['POST'])
@jwt_required
def phone_number():
    try:
        phone_number_2 = request.args.get('phone_number')
        phone_number_nationality = request.args.get('phone_number_nationality')
        user_id_assigned = request.args.get('user_id_assigned')
        forward_number = request.args.get('forward_number')
        mail = request.args.get('mail')
        auto_renewal = request.args.get('auto_renewal')

        # Special types
        db_phone_number = PhoneNumber(phone_number_2, phone_number_nationality)

        phone_number_registration = phone_number.PhoneNumber(
            phone_number=db_phone_number,
            user_id_assigned=user_id_assigned,
            forward_number=forward_number,
            mail=mail,
            auto_renewal=auto_renewal
        )

        db.session.add(phone_number_registration)
        db.session.commit()
        logging.info("Phone number %s was registered " % phone_number_registration.phone_number)
        return {'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_registration_route.route('/get_phone_number_by_id', methods=['GET'])
@jwt_required
def get_phone_number_by_id():
    phone_number_id = request.args.get('id')

    try:
        phone_number_company = PhoneNumber.find_by_id(phone_number_id)
        return jsonify(phone_number_company.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_registration_route.route('/get_phone_numbers', methods=['GET'])
@jwt_required
def get_phone_numbers():
    try:
        return {
            'phone_numbers': [e.serialize() for e in PhoneNumber.get_all_phone_numbers()]
        }
    except Exception as e:
        return {'message': str(e)}, 500
