from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import Forbidden
from gvo.exceptions.errors import NonUserPhoneError

from gvo.models.phone_number import PhoneNumber
from gvo.models.user import User


class UserValidator:
    @staticmethod
    def validate_user():
        firebase_id = get_jwt_identity()
        user = User.find_by_firebase_id(firebase_id)
        if user is None:
            raise Forbidden
        return user

    @staticmethod
    def validate_user_phone(user, user_phone):
        phone = PhoneNumber.find_by_phone(user_phone)
        if phone is None or phone.user_id_assigned != user.id:
            raise NonUserPhoneError
        return phone
