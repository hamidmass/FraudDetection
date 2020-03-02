import logging
from flask_jwt_extended import jwt_required
from sqlalchemy_utils import CurrencyType
from gvo.models import prepaid_account
from gvo.models.prepaid_account import PrepaidAccount
from flask import request, jsonify
from gvo.app import db
from flask import Blueprint

prepaid_account_route = Blueprint('prepaid_account', __name__)


@prepaid_account_route.route("/prepaid_account", methods=['GET', 'POST'])
@jwt_required
def add_prepaid_account():
    try:
        credit = request.args.get('credit')
        credit_currency_string = request.args.get('credit_currency')
        activated = request.args.get('activated')
        time_activated_epoch = request.args.get('time_activated_epoch')
        user_id_assigned = request.args.get('user_id_assigned')

        # Special types
        credit_currency = CurrencyType(credit_currency_string)

        company_user_table = prepaid_account.PrepaidAccount(
            credit=credit,
            credit_currency=credit_currency,
            activated=activated,
            time_activated_epoch=time_activated_epoch,
            user_id_assigned=user_id_assigned
        )

        db.session.add(company_user_table)
        db.session.commit()
        logging.info("Prepaid account was made with credit %s " % company_user_table.credit)
        return {'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@prepaid_account_route.route('/get_prepaid_account_by_id', methods=['GET'])
@jwt_required
def get_prepaid_account_by_id():
    prepaid_account_id = request.args.get('id')

    try:
        phone_number_transaction = PrepaidAccount.find_by_id(prepaid_account_id)
        return jsonify(phone_number_transaction.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@prepaid_account_route.route('/get_prepaid_accounts', methods=['GET'])
@jwt_required
def get_prepaid_accounts():
    try:
        return {
            'prepaid_accounts': [e.serialize() for e in PrepaidAccount.get_all_prepaid_accounts()]
        }
    except Exception as e:
        return {'message': str(e)}, 500
