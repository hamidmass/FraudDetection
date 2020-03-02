from gvo.models.fax_message import FaxMessage
from gvo.models.phone_number import PhoneNumber
from gvo.exceptions.errors import NonFaxPhoneError
from gvo.validators.user_validator import UserValidator


class FaxController:
    @staticmethod
    def send_fax(data, provider):
        user = UserValidator.validate_user()
        phone = UserValidator.validate_user_phone(user, data.origin_phone)
        if not phone.is_fax:
            raise NonFaxPhoneError
        fax_message = FaxMessage(origin_phone=data.origin_phone,
                                 destination_phone=data.destination_phone,
                                 url=data.fax_url)
        provider.send_fax(fax_message)

    @staticmethod
    def receive_fax(fax, provider):
        phone = PhoneNumber.find_by_phone(fax.destination_phone)
        if phone:
            response = provider.accept_fax('fax/received')
        else:
            response = provider.reject_fax()
        return response
