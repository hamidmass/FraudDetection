import logging
from flask import request, jsonify
from gvo.app import db
from gvo.models import phone_number_owner_user, phone_number_owner_company
from gvo.models.phone_number_owner_user import PhoneNumberOwnerUser
from gvo.models.phone_number_owner_company import PhoneNumberOwnerCompany
from flask_jwt_extended import  jwt_required
from flask import Blueprint

phone_number_owner_route = Blueprint('phone_number_owner', __name__)


@phone_number_owner_route.route('/phone_number_user_registration', methods=['POST'])
@jwt_required
def phone_number_user_registration():
    try:
        user_id = request.args.get('user-id')
        phone_number_id = request.args.get('phone-number-id')

        phone_number_owner_user_table = phone_number_owner_user.PhoneNumberOwnerUser(
            user_id=user_id,
            phone_number_id=phone_number_id
        )

        db.session.add(phone_number_owner_user_table)
        db.session.commit()
        logging.info("Phone number id %s is registered for user %s " % phone_number_owner_user_table.user_id
                     % phone_number_owner_user_table.phone_number_id)
        return {'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_owner_route.route('/phone_number_company_registration', methods=['POST'])
@jwt_required
def phone_number_company_registration():
    try:
        company_id = request.args.get('company-id')
        phone_number_id = request.args.get('phone-number-id')

        phone_number_owner_company_table = phone_number_owner_company.PhoneNumberOwnerCompany(
            company_id=company_id,
            phone_number_id=phone_number_id
        )

        db.session.add(phone_number_owner_company_table)
        db.session.commit()
        logging.info("Phone number id %s is registered for company %s " % phone_number_owner_company_table.user_id
                     % phone_number_owner_company_table.phone_number_id)
        return {'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_owner_route.route('/get_phone_number_owner_user_by_id', methods=['GET'])
@jwt_required
def get_phone_number_owner_user_by_id():
    user_id = request.args.get('id')

    try:
        phone_number_owner = PhoneNumberOwnerUser.find_by_id(user_id)
        return jsonify(phone_number_owner.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_owner_route.route('/get_phone_number_owner_users', methods=['GET'])
@jwt_required
def get_phone_number_owner_users():
    try:
        return {
            'phone_number_owners': [e.serialize() for e in PhoneNumberOwnerUser.get_all_phone_owners()]
        }
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_owner_route.route('/get_phone_number_owner_company_by_id', methods=['GET'])
@jwt_required
def get_phone_number_owner_company_by_id():
    company_id = request.args.get('id')

    try:
        phone_number_company = PhoneNumberOwnerUser.find_by_id(company_id)
        return jsonify(phone_number_company.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_owner_route.route('/get_phone_number_owner_companies', methods=['GET'])
@jwt_required
def get_phone_number_owner_companies():
    try:
        return {
            'phone_number_owners': [e.serialize() for e in PhoneNumberOwnerCompany.get_all_phone_owners()]
        }
    except Exception as e:
        return {'message': str(e)}, 500
