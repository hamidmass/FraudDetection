from flask import Blueprint
from flask import request, Response
from flask_jwt_extended import jwt_required


from gvo.app import twilio
from gvo.validators.twilio_validator import TwilioValidator
from gvo.controllers.mail_controller import MailController
from gvo.parsers.fax_parser import FaxParser
from gvo.controllers.fax_controller import FaxController


twilio_fax = Blueprint('twilio_fax', __name__)


@twilio_fax.route("/fax/send", methods=['POST'])
@jwt_required
def send_fax():
    data = FaxParser(request)
    FaxController.send_fax(data, twilio)
    return '', 200


@twilio_fax.route("/fax/sent", methods=['POST'])
@TwilioValidator.validate_request
def fax_sent():
    fax = twilio.receive_fax(request)
    response = FaxController.receive_fax(fax, twilio)
    return Response(response, mimetype='text/xml')


@twilio_fax.route('/fax/received', methods=['POST'])
@TwilioValidator.validate_request
def fax_received():
    fax = twilio.receive_fax(request)
    MailController.send_email(fax)
    return '', 200
