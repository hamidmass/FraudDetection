import requests
from flask import request, jsonify
from gvo.app import firebase
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import Blueprint

user_login = Blueprint('login', __name__)


@user_login.route('/login', methods=['POST'])
def login():
    firebase_id = request.args.get('firebase_id', None)
    access_token = create_access_token(identity=firebase_id)
    refresh_token = create_refresh_token(identity=firebase_id)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token, "msg": None}), 200

