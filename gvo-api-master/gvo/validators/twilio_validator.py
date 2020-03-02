import os

from twilio.request_validator import RequestValidator
from functools import wraps
from flask import abort, request
from gvo.validators.provider_validator import ProviderValidator


class TwilioValidator(ProviderValidator):
    @staticmethod
    def validate_request(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            validator = RequestValidator(os.getenv('TWILIO_AUTH_TOKEN'))

            request_valid = validator.validate(
                request.url,
                request.form,
                request.headers.get('X-TWILIO-SIGNATURE', ''))

            if request_valid:
                return function(*args, **kwargs)
            else:
                return abort(403)
        return decorated_function
