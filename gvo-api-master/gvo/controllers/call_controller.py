from gvo.models.phone_number import PhoneNumber
from gvo.validators.user_validator import UserValidator


class CallController:
    @staticmethod
    def start_inbound_call(data, provider):
        phone = PhoneNumber.find_by_phone(data.destination_phone)
        # TODO: change the verification, verifying if the number has the call forward service
        if phone and phone.forward_number:
            response = provider.start_call_forward(phone.forward_number, "inbound-call/end")
        # TODO: change the verification, verifying if the number has the voicemail service
        elif phone and phone.mail:
            response = provider.redirect_to_voicemail("inbound-call/end")
        else:
            response = provider.finish_call()
        return response

    @staticmethod
    def end_inbound_call(data, provider):
        phone = PhoneNumber.find_by_phone(data.destination_phone)
        # TODO: change the verification, verifying if the number has the voice mail service
        if phone and phone.mail:
            response = provider.end_call_forward(data.call_status, "inbound-call/voice-mail")
        else:
            response = provider.finish_call()
        return response

    @staticmethod
    def start_outbound_call(data, provider):
        user = UserValidator.validate_user()
        UserValidator.validate_user_phone(user, data.origin_phone)
        provider.make_call(data.origin_phone, data.destination_phone, "outbound-call/redirect")

    @staticmethod
    def redirect_outbound_call(data, provider):
        phone = PhoneNumber.find_by_phone(data.origin_phone)
        if phone and phone.forward_number:
            response = provider.redirect_call(data.call_status, phone.forward_number)
        else:
            response = provider.finish_call()
        return response
