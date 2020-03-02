import logging
import requests
from sqlalchemy_utils import PhoneNumber, Country
from gvo.models import company, company_user
from gvo.models.company import Company
from flask import request, jsonify
from gvo.app import db, firebase
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from flask import Blueprint

company_route = Blueprint('company', __name__)


@company_route.route("/add_company", methods=['GET', 'POST'])
def add_company():
    company_name = request.args.get('name')
    email = request.args.get('email')
    street = request.args.get('street')
    zip = request.args.get('zip')
    city = request.args.get('city')
    country = request.args.get('country')
    phone_number = request.args.get('phone_number')
    phone_number_nationality = request.args.get('phone_number_nationality')
    vat_number = request.args.get('vat_number')
    firebase_id_company = request.args.get('firebase_id')

    #username = request.args.get('username', None)
    #password = request.args.get('password', None)
    #if not username:
    #    return jsonify({"msg": "Missing username parameter"}), 400
    #if not password:
    #    return jsonify({"msg": "Missing password parameter"}), 400

    try:
        ## Get a reference to the auth service
        #auth = firebase.auth()
#
        ## Send login to firebase
        #try:
        #    firebase_user = auth.create_user_with_email_and_password(username, password)
        #except requests.exceptions.HTTPError as error:
        #    return jsonify({"msg": "Error:  " + str(error)}), 400
#
        #firebase_id_company = str(firebase_user['localId'])

        # Special types
        phone_number_column = PhoneNumber(phone_number, phone_number_nationality)
        country_column = Country(str(country))

        # Add the user into the database
        company_table = company.Company(
            name=company_name,
            email=email,
            street=street,
            zip=zip,
            city=city,
            country=country_column,
            phone_number=phone_number_column,
            vat_number=vat_number,
            firebase_id_company=firebase_id_company
        )

        db.session.add(company_table)
        db.session.commit()
        logging.info("Company %s was created" % company_table.company_name)

        # JWT
        access_token = create_access_token(identity=firebase_id_company)
        refresh_token = create_refresh_token(identity=firebase_id_company)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    except Exception as e:
        return {'message': str(e)}, 500


@company_route.route("/add_company_user", methods=['GET', 'POST'])
@jwt_required
def add_company_user():
    try:
        company_id = request.args.get('company_id')
        user_id = request.args.get('user_id')

        company_user_table = company_user.CompanyUser(
            company_id=company_id,
            user_id=user_id
        )

        db.session.add(company_user_table)
        db.session.commit()
        logging.info("User with id %s was added to company" % company_user_table.company_id
                     % company_user_table.user_id)
        return {'success', 400}
    except Exception as e:
        return {'message': str(e)}, 500


@company_route.route('/get_company_by_id', methods=['GET'])
@jwt_required
def get_company_by_id():
    company_id = request.args.get('company_id')

    try:
        current_user = Company.find_by_id(company_id)
        return jsonify(current_user.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@company_route.route('/get_company_name', methods=['GET'])
@jwt_required
def get_company_by_name():
    name = request.args.get('name')

    try:
        current_company = Company.find_by_name(name)
        return current_company.serialize()
    except Exception as e:
        return {'message': str(e)}, 500


@company_route.route('/get_all_companies', methods=['GET'])
@jwt_required
def get_all_companies():
    try:
        return {
            'users': [e.serialize() for e in Company.get_all_companies()]
        }
    except Exception as e:
        return {'message': str(e)}, 500