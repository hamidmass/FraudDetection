from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required

from gvo.app import twilio
from gvo.controllers.sms_controller import SmsController
from gvo.parsers.sms_parser import SmsParser

twilio_sms = Blueprint('twilio_sms', __name__)


@twilio_sms.route("/sms/send", methods=["POST"])
@jwt_required
def send_sms():
    data = SmsParser(request)
    SmsController.send_sms(data, twilio)
    return "", '200'
