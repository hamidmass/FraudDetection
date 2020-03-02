from sqlalchemy_utils import PhoneNumber
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from gvo.exceptions.errors import EmptySmsError, InvalidPhoneNumberError


class SmsParser:
    def __init__(self, request):
        self.sms = request.form.get('sms')
        if not self.sms:
            raise EmptySmsError
        try:
            self.origin_phone = PhoneNumber(request.form.get('origin_phone'))
            self.destination_phone = PhoneNumber(request.form.get('destination_phone'))
        except PhoneNumberParseException:
            raise InvalidPhoneNumberError
