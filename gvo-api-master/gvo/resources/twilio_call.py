from flask import Blueprint
from flask import request, Response
from flask_jwt_extended import jwt_required


from gvo.app import twilio
from gvo.validators.twilio_validator import TwilioValidator
from gvo.controllers.mail_controller import MailController
from gvo.parsers.call_parser import CallParser
from gvo.controllers.call_controller import CallController

twilio_call = Blueprint('twilio_call', __name__)


@twilio_call.route("/inbound-call/start", methods=['POST'])
@TwilioValidator.validate_request
def start_call():
    data = CallParser(request)
    response = CallController.start_inbound_call(data, twilio)
    return Response(response, mimetype='text/xml')


@twilio_call.route("/inbound-call/end", methods=['POST'])
@TwilioValidator.validate_request
def end_call():
    data = CallParser(request)
    response = CallController.end_inbound_call(data, twilio)
    return Response(response, mimetype='text/xml')


@twilio_call.route("/inbound-call/voice-mail", methods=['POST'])
@TwilioValidator.validate_request
def send_voice_mail():
    voice_mail = twilio.receive_voicemail(request)
    MailController.send_email(voice_mail)
    return '', 200


@twilio_call.route("/outbound-call", methods=['POST'])
@jwt_required
def start_outbound_call():
    data = CallParser(request)
    CallController.start_outbound_call(data, twilio)
    return '', 204


@twilio_call.route("/outbound-call/redirect", methods=['POST'])
@TwilioValidator.validate_request
def redirect_outbound_call():
    data = CallParser(request)
    response = CallController.redirect_outbound_call(data, twilio)
    return Response(response, mimetype='text/xml')
