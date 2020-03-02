from gvo.validators.user_validator import UserValidator


class SmsController:
    @staticmethod
    def send_sms(data, provider):
        user = UserValidator.validate_user()
        UserValidator.validate_user_phone(user, data.origin_phone)
        provider.send_sms(data.origin_phone, data.destination_phone, data.sms)
