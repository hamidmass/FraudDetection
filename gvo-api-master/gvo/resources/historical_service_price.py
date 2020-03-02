import datetime
import logging
from flask import request, jsonify
from sqlalchemy_utils import Country, Currency
from gvo.app import db
from gvo.models import historical_service_price
from gvo.models.historical_service_price import HistoricalServicePrice
from gvo.models.service_name_enum import ServiceNameEnum
from flask_jwt_extended import jwt_required
from flask import Blueprint

historical_service_price_route = Blueprint('historical_service_price', __name__)


@historical_service_price_route.route('/historical_service_price', methods=['POST'])
@jwt_required
def add_historical_service_price():
    try:
        service_name_enum = request.args.get('service_name_enum')
        country = request.args.get('country')
        region = request.args.get('region')
        time_epoch = request.args.get('time_epoch')
        price = request.args.get('price')
        currency = request.args.get('currency')

        # Special types
        time_epoch_column = datetime.datetime.fromtimestamp(int(time_epoch))
        service_name_enum_column = ServiceNameEnum(int(service_name_enum))
        country_column = Country(str(country))
        currency_column = Currency(str(currency))

        subscription_company_table = historical_service_price.HistoricalServicePrice(
            service_name_enum=service_name_enum_column,
            country=country_column,
            region=region,
            time_epoch=time_epoch_column,
            price=price,
            currency=currency_column
        )

        db.session.add(subscription_company_table)
        db.session.commit()
        logging.info("Historical service price was registered")
        return {'message': 'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


@historical_service_price_route.route('/get_service_price_by_id', methods=['GET'])
@jwt_required
def get_company_by_id():
    service_id = request.args.get('id')

    try:
        historical_price = HistoricalServicePrice.find_by_id(service_id)
        return jsonify(historical_price.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@historical_service_price_route.route('/get_all_service_prices', methods=['GET'])
@jwt_required
def get_all_companies():
    try:
        return {
            'service_prices': [e.serialize() for e in HistoricalServicePrice.get_all_service_prices()]
        }
    except Exception as e:
        return {'message': str(e)}, 500

