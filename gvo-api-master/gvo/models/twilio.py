import os
from dotenv import load_dotenv
from sqlalchemy_utils import PhoneNumber

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.fax_response import FaxResponse

from gvo.models.fax_message import FaxMessage
from gvo.models.voice_message import VoiceMessage

load_dotenv()

PHONE_LIST_SIZE_LIMIT = 20
BASE_URL = os.getenv('BASE_URL')
VOICE_URL = {"fax": "fax/sent", "voice": "inbound-call/start"}
VOICEMAIL_MAX_LENGTH = "60"


class Twilio:
    def __init__(self):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.client = Client(account_sid, auth_token)

    def search_phone_numbers(self, options):
        if options.type == "mobile":
            phones = self.client.available_phone_numbers(options.country_code).mobile
        elif options.type == "toll free":
            phones = self.client.available_phone_numbers(options.country_code).toll_free
        else:
            phones = self.client.available_phone_numbers(options.country_code).local
        phones = phones.list(limit=PHONE_LIST_SIZE_LIMIT,
                             fax_enabled=options.fax_enabled,
                             sms_enabled=options.sms_enabled,
                             voice_enabled=options.voice_enabled)
        return phones

    def buy_phone_number(self, phone, phone_type):
        incoming_phone_number = self.client.incoming_phone_numbers.create(
            phone_number=phone.e164,
            voice_receive_mode=phone_type,
            voice_url=BASE_URL + VOICE_URL[phone_type]
        )
        return incoming_phone_number

    def update_phone_number(self, phone, phone_type):
        self.client.incoming_phone_numbers(phone.sid).update(
            voice_receive_mode=phone_type,
            voice_url=BASE_URL + VOICE_URL[phone_type])

    def delete_phone_number(self, phone):
        self.client.incoming_phone_numbers(phone.sid).delete()

    def make_call(self, origin_phone, destination_phone, extension_url):
        self.client.calls.create(
                        url=BASE_URL + extension_url,
                        to= destination_phone.e164,
                        from_=origin_phone.e164
                    )

    def send_sms(self, origin_phone, destination_phone, sms):
        header = "---Message send from {}---\n\n".format(origin_phone.e164)
        message = self.client.messages.create(
            body=header + sms,
            from_=origin_phone.e164,
            to=destination_phone.e164
        )
        return message

    def send_fax(self, fax_message):
        fax = self.client.fax.faxes.create(
            from_=fax_message.origin_phone.e164,
            to=fax_message.destination_phone.e164,
            media_url=fax_message.file_url
        )
        return fax

    def receive_fax(self, request):
        origin_phone = PhoneNumber(request.form.get('From'))
        destination_phone = PhoneNumber(request.form.get('To'))
        file_url = request.form.get('MediaUrl')
        return FaxMessage(origin_phone=origin_phone, destination_phone=destination_phone, url=file_url)

    def receive_voicemail(self, request):
        origin_phone = PhoneNumber(request.form.get('From'))
        destination_phone = PhoneNumber(request.form.get('To'))
        file_url = request.form.get('RecordingUrl')
        return VoiceMessage(origin_phone=origin_phone, destination_phone=destination_phone, url=file_url)

    def accept_fax(self, extension_url):
        response = FaxResponse()
        # We accept it and indicate the url callback
        response.receive(action=BASE_URL + extension_url)
        return str(response)

    def reject_fax(self):
        response = VoiceResponse()
        response.reject()
        return str(response)

    def start_call_forward(self, phone, extension_url):
        response = VoiceResponse()
        response.dial(number=phone.e164, action=BASE_URL + extension_url)
        return str(response)

    def end_call_forward(self, call_status, extension_url):
        response = VoiceResponse()
        if call_status != "completed":
            response.say("Please leave a message at the beep.")
            response.record(max_length=VOICEMAIL_MAX_LENGTH, action=BASE_URL + extension_url)
        response.hangup()
        return str(response)

    def finish_call(self):
        response = VoiceResponse()
        response.hangup()
        return str(response)

    def redirect_to_voicemail(self, extension_url):
        response = VoiceResponse()
        response.redirect(BASE_URL + extension_url)
        return str(response)

    def redirect_call(self, call_status, phone):
        response = VoiceResponse()
        if call_status == 'in-progress':
            response.dial(number=phone.e164)
        else:
            response.hangup()
        return str(response)
