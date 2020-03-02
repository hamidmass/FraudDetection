import logging
from flask import request, jsonify
from gvo.app import db
from gvo.models import subscription_company, subscription_user
from gvo.models.subscription_user import SubscriptionUser
from gvo.models.subscription_company import SubscriptionCompany
from flask_jwt_extended import  jwt_required
from flask import Blueprint

subscription_route = Blueprint('subscription', __name__)


@subscription_route.route('/subscription_company', methods=['POST'])
@jwt_required
def add_subscription_company():
    try:
        service_name_enum = request.args.get('service_name_enum')
        company_id = request.args.get('company_id')
        user_id_assigned = request.args.get('user_id_assigned')
        mail = request.args.get('mail')
        auto_renewal = request.args.get('auto_renewal')

        subscription_company_table = subscription_company.SubscriptionCompany(
            service_name_enum=service_name_enum,
            company_id=company_id,
            user_id_assigned=user_id_assigned,
            mail=mail,
            auto_renewal=auto_renewal
        )

        db.session.add(subscription_company_table)
        db.session.commit()
        logging.info("Subscription for company mail %s was made" % subscription_company_table.mail)
        return {'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@subscription_route.route('/subscription_user', methods=['POST'])
@jwt_required
def add_subscription_user():
    try:
        service_name_enum = request.args.get('service_name_enum')
        user_id = request.args.get('user_id')
        user_id_assigned = request.args.get('user_id_assigned')
        mail = request.args.get('mail')
        auto_renewal = request.args.get('auto_renewal')

        subscription_user_table = subscription_user.SubscriptionUser(
            service_name_enum=service_name_enum,
            user_id=user_id,
            user_id_assigned=user_id_assigned,
            mail=mail,
            auto_renewal=auto_renewal
        )

        db.session.add(subscription_user_table)
        db.session.commit()
        logging.info("Subscription for user mail %s was made" % subscription_user_table.mail)
        return {'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@subscription_route.route('/get_subscription_user_by_id', methods=['GET'])
@jwt_required
def get_subscription_user_by_id():
    user_id = request.args.get('id')

    try:
        subscription_user_id = SubscriptionUser.find_by_id(user_id)
        return jsonify(subscription_user_id.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@subscription_route.route('/get_subscription_users', methods=['GET'])
@jwt_required
def get_subscription_users():
    try:
        return {
            'subscription_users': [e.serialize() for e in SubscriptionUser.get_all_subscriptions()]
        }
    except Exception as e:
        return {'message': str(e)}, 500


@subscription_route.route('/get_subscription_company_by_id', methods=['GET'])
@jwt_required
def get_subscription_company_by_id():
    company_id = request.args.get('id')

    try:
        subscription_company_id = SubscriptionCompany.find_by_id(company_id)
        return jsonify(subscription_company_id.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@subscription_route.route('/get_subscription_companies', methods=['GET'])
@jwt_required
def get_subscription_companies():
    try:
        return {
            'subscription_users': [e.serialize() for e in SubscriptionCompany.get_all_subscriptions()]
        }
    except Exception as e:
        return {'message': str(e)}, 500

