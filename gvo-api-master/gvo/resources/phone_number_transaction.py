import logging
from flask import request, jsonify
from sqlalchemy_utils import PhoneNumber
from gvo.app import db
from gvo.models import phone_number_transaction_company, phone_number_transaction_user
from gvo.models.phone_number_transaction_user import PhoneNumberTransactionUser
from gvo.models.phone_number_transaction_company import PhoneNumberTransactionCompany
from flask_jwt_extended import jwt_required
from flask import Blueprint

phone_number_transaction_route = Blueprint('phone_number_transaction', __name__)


@phone_number_transaction_route.route('/phone_number_transaction_company', methods=['POST'])
@jwt_required
def phone_number_transaction_company():
    try:
        phone_number_req = request.args.get('phone_number')
        phone_number_nationality = request.args.get('phone_number_nationality')
        company_id = request.args.get('company_id')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        # Special types
        db_phone_number = PhoneNumber(phone_number_req, phone_number_nationality)

        company_user_table = phone_number_transaction_company.PhoneNumberTransactionCompany(
            phone_number=db_phone_number,
            company_id=company_id,
            start_time=start_time,
            end_time=end_time
        )

        db.session.add(company_user_table)
        db.session.commit()
        logging.info("Company transaction with phone number %s " % company_user_table.phone_number)
        return {'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_transaction_route.route('/phone_number_transaction_user', methods=['POST'])
@jwt_required
def phone_number_transaction_user():
    try:
        phone_number_req = request.args.get('phone_number')
        phone_number_nationality = request.args.get('phone_number_nationality')
        user_id = request.args.get('user_id')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        # Special types
        db_phone_number = PhoneNumber(phone_number_req, phone_number_nationality)

        company_transaction_table = phone_number_transaction_user.PhoneNumberTransactionUser(
            phone_number=db_phone_number,
            user_id=user_id,
            start_time=start_time,
            end_time=end_time
        )

        db.session.add(company_transaction_table)
        db.session.commit()
        logging.info("User transaction with phone number %s " % company_transaction_table.phone_number)
        return {'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_transaction_route.route('/get_phone_number_transaction_user_by_id', methods=['GET'])
@jwt_required
def get_phone_number_transaction_user_by_id():
    transaction_id = request.args.get('id')

    try:
        phone_number_transaction = PhoneNumberTransactionUser.find_by_id(transaction_id)
        return jsonify(phone_number_transaction.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_transaction_route.route('/get_phone_number_transaction_users', methods=['GET'])
@jwt_required
def get_phone_number_transaction_users():
    try:
        return {
            'phone_number_transactions': [e.serialize() for e in PhoneNumberTransactionUser.get_all_transactions()]
        }
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_transaction_route.route('/get_phone_number_transaction_company_by_id', methods=['GET'])
@jwt_required
def get_phone_number_transaction_company_by_id():
    transaction_id = request.args.get('id')

    try:
        phone_number_transaction = PhoneNumberTransactionCompany.find_by_id(transaction_id)
        return jsonify(phone_number_transaction.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@phone_number_transaction_route.route('/get_phone_number_transaction_companies', methods=['GET'])
@jwt_required
def get_phone_number_transaction_companies():
    try:
        return {
            'phone_number_transactions': [e.serialize() for e in PhoneNumberTransactionCompany.get_all_transactions()]
        }
    except Exception as e:
        return {'message': str(e)}, 500
