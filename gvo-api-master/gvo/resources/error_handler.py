from flask import Blueprint
from flask import jsonify

from twilio.base.exceptions import TwilioRestException, TwilioException
from werkzeug.exceptions import HTTPException

from gvo.exceptions.errors import GvoApiError

error_handler = Blueprint('error_handler', __name__)


def response_error(error):
    message = [str(x) for x in error.args]
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        },
    }
    return response


@error_handler.app_errorhandler(TwilioRestException)
def handle_error(error):
    status_code = error.status
    response = response_error(error)
    return jsonify(response), status_code


@error_handler.app_errorhandler(TwilioException)
def handle_error(error):
    status_code = error.args[1].status_code
    response = response_error(error)
    return jsonify(response), status_code


@error_handler.app_errorhandler(GvoApiError)
def handle_error(error):
    status_code = 404
    response = response_error(error)
    return jsonify(response), status_code


@error_handler.app_errorhandler(HTTPException)
def handle_error(error):
    error.args = (error.description,)
    status_code = error.code
    response = response_error(error)
    return jsonify(response), status_code


@error_handler.app_errorhandler(Exception)
def handle_error(error):
    status_code = 500
    response = response_error(error)
    return jsonify(response), status_code
