import logging

from gvo.models.phone_number import PhoneNumber
from gvo.helpers.phone_list import PhoneList
from gvo.validators.user_validator import UserValidator
from gvo.exceptions.errors import InvalidPhoneTypeError
from gvo.app import db

VALID_PHONE_TYPES = ["fax", "voice"]


class PhoneController:
    @staticmethod
    def search_phones(data, provider):
        phones = provider.search_phone_numbers(data)
        return PhoneList.json(phones)

    @staticmethod
    def buy_phone(user, data, provider):
        if data.phone_type not in VALID_PHONE_TYPES:
            raise InvalidPhoneTypeError
        phone = provider.buy_phone_number(data.phone_number, data.phone_type)
        db_phone = PhoneNumber(
            phone_number=phone.phone_number,
            user_id_assigned=user.id,
            forward_number=data.forward_number,
            mail=data.mail,
            auto_renewal=False,  # TODO: replace it for the correct value
            sid=phone.sid,
            is_fax=data.phone_type == 'fax'
        )
        db.session.add(db_phone)
        db.session.commit()
        logging.info("Phone number {} was added to the user {}".format(data.phone_number.e164, user))

    @staticmethod
    def update_phone(data, provider):
        if data.phone_type not in VALID_PHONE_TYPES:
            raise InvalidPhoneTypeError
        user = UserValidator.validate_user()
        phone = UserValidator.validate_user_phone(user, data.phone_number)
        provider.update_phone_number(phone, data.phone_type)
        phone.forward_number = data.forward_number
        phone.mail = data.mail
        phone.is_fax = data.phone_type == 'fax'
        db.session.commit()

    @staticmethod
    def delete_phone(data, provider):
        user = UserValidator.validate_user()
        phone = UserValidator.validate_user_phone(user, data.phone_number)
        provider.delete_phone_number(phone)
        db.session.delete(phone)
        db.session.commit()
        logging.info("The phone number {} was removed from user {}".format(data.phone_number.e164, user))

    @staticmethod
    def get_phone_numbers(user, phone_type):
        is_fax = phone_type == 'fax'
        phones = list(filter(lambda phone: phone.is_fax == is_fax, PhoneNumber.find_by_user_id(user.id)))
        return [phone.serialize() for phone in phones]
