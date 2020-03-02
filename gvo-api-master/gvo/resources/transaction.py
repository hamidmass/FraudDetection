import datetime
import logging
from flask import request, jsonify
from gvo.app import db
from gvo.models import transaction, transaction_user, transaction_company
from gvo.models.transaction import Transaction
from gvo.models.transaction_user import TransactionUser
from gvo.models.transaction_company import TransactionCompany
from gvo.models.service_name_enum import ServiceNameEnum
from flask_jwt_extended import jwt_required
from flask import Blueprint

transaction_route = Blueprint('transaction', __name__)


@transaction_route.route('/transaction_company', methods=['POST'])
@jwt_required
def do_transaction_company():
    try:
        company_id = request.args.get('company_id')
        transaction_id = do_transaction()

        transaction_company_row = transaction_company.TransactionCompany(
            company_id=company_id,
            transaction_id=transaction_id
        )

        db.session.add(transaction_company_row)
        db.session.commit()
        logging.info("Transaction for Company with id %s was made" % transaction_company_row.company_id)
        return {'message': 'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@transaction_route.route('/transaction_user', methods=['POST'])
@jwt_required
def do_transaction_user():
    try:
        user_id = request.args.get('user_id')
        transaction_id = do_transaction()

        transaction_user_row = transaction_user.TransactionUser(
            user_id=user_id,
            transaction_id=transaction_id
        )

        db.session.add(transaction_user_row)
        db.session.commit()
        logging.info("Transaction for User with id %s was made" % transaction_user_row.user_id)
        return {'message': 'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


def do_transaction():
    service_name_enum = request.args.get('service_name_enum')
    user_id_assigned = request.args.get('user_id_assigned')
    mail = request.args.get('mail')
    historical_service_price_id = request.args.get('historical_service_price_id')
    country = request.args.get('country')
    region = request.args.get('region')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Special types
    start_time_column = datetime.datetime.fromtimestamp(int(start_time))
    end_time_column = datetime.datetime.fromtimestamp(int(end_time))
    service_name_enum_column = ServiceNameEnum(int(service_name_enum))

    company_user_table = transaction.Transaction(
        service_name_enum=service_name_enum_column,
        user_id_assigned=user_id_assigned,
        mail=mail,
        historical_service_price_id=historical_service_price_id,
        country=country,
        region=region,
        start_time=start_time_column,
        end_time=end_time_column
    )

    db.session.add(company_user_table)
    db.session.commit()
    return company_user_table.id


@transaction_route.route('/get_transaction_user_by_id', methods=['GET'])
@jwt_required
def get_transaction_user_by_id():
    transaction_user_id = request.args.get('id')

    try:
        # Joining the TransactionUser table with Transaction
        test = db.session.query(TransactionUser, Transaction).join(Transaction)\
            .filter(TransactionUser.transaction_id == Transaction.id
                    and TransactionUser.user_id == transaction_user_id)\
            .one()
        transaction_user_result = test[0]
        transaction_result = test[1]

        result1 = transaction_user_result.serialize()
        result2 = transaction_result.serialize()

        transaction_merged = {**result1, **result2}

        return {"transaction": transaction_merged}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@transaction_route.route('/get_transaction_company_by_id', methods=['GET'])
@jwt_required
def get_transaction_company_by_id():
    transaction_company_id = request.args.get('id')

    try:
        # Joining the TransactionUser table with Transaction
        test = db.session.query(TransactionCompany, Transaction).join(Transaction) \
            .filter(TransactionCompany.transaction_id == Transaction.id
                    and TransactionCompany.company_id == transaction_company_id) \
            .one()
        transaction_user_result = test[0]
        transaction_result = test[1]

        result1 = transaction_user_result.serialize()
        result2 = transaction_result.serialize()

        transaction_merged = {**result1, **result2}

        return {"transaction": transaction_merged}, 400
    except Exception as e:
        return {'message': str(e)}, 500


