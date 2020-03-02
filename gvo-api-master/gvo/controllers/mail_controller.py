from gvo.models.phone_number import PhoneNumber
from gvo.app import email_sender
from gvo.exceptions.errors import NonExistentPhoneError


class MailController:
    @staticmethod
    def send_email(file):
        phone = PhoneNumber.find_by_phone(file.destination_phone)
        if phone is None:
            raise NonExistentPhoneError
        email_sender.send_email(file, phone.mail)

