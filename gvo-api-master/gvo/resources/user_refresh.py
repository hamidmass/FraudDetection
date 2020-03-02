from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity


from flask import Blueprint

user_refresh = Blueprint('refresh', __name__)

# User needs to have valid refresh token
# to get a new one
@user_refresh.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    firebase_id = get_jwt_identity()
    access_token = create_access_token(identity=firebase_id)
    return jsonify({"access_token": access_token}), 200
