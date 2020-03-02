import requests
from gvo.models.user import User
from flask import request, jsonify
from flask_jwt_extended import (jwt_required)
from flask import Blueprint

users = Blueprint('user_query', __name__)


@users.route("/user_by_id", methods=['GET'])
@jwt_required
def get_user_by_id():
    user_id = request.args.get('user_id')

    try:
        current_user = User.find_by_id(user_id)
        return jsonify(current_user.serialize())
    except Exception as e:
        return {'message': str(e)}, 500


@users.route('/users', methods=['GET'])
@jwt_required
def get_all_users():
    try:
        return {
            'users': [e.serialize() for e in User.get_all_users()]
        }
    except Exception as e:
        return {'message': str(e)}, 500
