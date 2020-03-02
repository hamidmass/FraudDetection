from sqlalchemy_utils import PhoneNumber
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from gvo.exceptions.errors import EmptyFaxError, InvalidPhoneNumberError


class FaxParser:
    def __init__(self, request):
        self.fax_url = request.form.get('fax_message')
        if not self.fax_url:
            raise EmptyFaxError
        try:
            self.origin_phone = PhoneNumber(request.form.get('origin_phone'))
            self.destination_phone = PhoneNumber(request.form.get('destination_phone'))
        except PhoneNumberParseException:
            raise InvalidPhoneNumberError
