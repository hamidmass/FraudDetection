import logging

import requests
from sqlalchemy_utils import PhoneNumber, CountryType, CurrencyType
from gvo.models import user
from flask import request, jsonify
from gvo.app import db, firebase
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from flask import Blueprint

user_registration_route = Blueprint('user_registration', __name__)


@user_registration_route.route("/add_user", methods=['GET', 'POST'])
def add_user():
    email = request.args.get('email')
    phone_number = request.args.get('phone_number')
    phone_number_nationality = request.args.get('phone_number_nationality')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    civility = request.args.get('civility')
    street = request.args.get('street')
    zip = request.args.get('zip')
    city = request.args.get('city')
    country = request.args.get('country')
    credit = request.args.get('credit', None)
    credit_currency = request.args.get('credit_currency', None)
    firebase_id = request.args.get('firebase_id', None)

    try:
        # Special types
        db_phone_number = PhoneNumber(phone_number, phone_number_nationality)
        db_country = CountryType(str(country))
        db_currency = CurrencyType(str(credit_currency))

        # Add the user into the database
        user_table = user.User(
            email=email,
            phone_number=db_phone_number,
            first_name=first_name,
            last_name=last_name,
            civility=civility,
            street=street,
            zip=zip,
            city=city,
            country=db_country,
            credit=credit,
            credit_currency=db_currency,
            firebase_id=firebase_id
        )

        db.session.add(user_table)
        db.session.commit()
        logging.info("User %s was created" % user_table.email)

        # JWT
        access_token = create_access_token(identity=firebase_id)
        refresh_token = create_refresh_token(identity=firebase_id)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200)
    except Exception as e:
        print("Error: " + str(e))
        return jsonify({'message': str(e)}, 500)


@user_registration_route.route("/upload_user_identification", methods=['GET', 'POST'])
@jwt_required
def upload_user_identification():
    email = request.args.get('email')

    try:
        for upload in request.files.getlist("file"):
            logging.info("Got file upload for user mail %s" % email)
            filename = upload.filename
            print("Got file: " + filename)
            # Update the user
            update_user = user.User.query.filter_by(email=email).first()
            update_user.identification_filename = filename
            update_user.identification_binary = upload.read()
            db.session.commit()
            logging.info("User %s was updated with identification" % update_user.email)
        return {'message': 'success'}, 200
    except Exception as e:
        return {'message': str(e)}, 500


@user_registration_route.route("/upload_proof_of_address", methods=['GET', 'POST'])
@jwt_required
def upload_user_proof_of_address():
    email = request.args.get('email')

    try:
        for upload in request.files.getlist("file"):
            logging.info("Got file upload for user mail %s" % email)
            filename = upload.filename
            print("Got file: " + filename)
            # Update the user
            update_user = user.User.query.filter_by(email=email).first()
            update_user.proof_of_address_name = filename
            update_user.proof_of_address_binary = upload.read()
            db.session.commit()
            logging.info("User %s was updated with identification" % update_user.email)
        return {'message': 'success'}, 400
    except Exception as e:
        return {'message': str(e)}, 500
