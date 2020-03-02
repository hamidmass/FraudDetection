from sqlalchemy_utils import PhoneNumber
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from gvo.exceptions.errors import InvalidPhoneNumberError


class PhoneParser:
    def __init__(self, request):
        self.phone_type = request.form.get("phone_type")
        self.forward_number = request.form.get("forward_number")
        self.mail = request.form.get("mail")
        try:
            self.phone_number = PhoneNumber(request.form.get("phone_number"))
        except PhoneNumberParseException:
            raise InvalidPhoneNumberError
