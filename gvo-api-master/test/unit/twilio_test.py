import os

from twilio.rest.api.v2010.account.message import MessageInstance
from twilio.rest.api.v2010.account.incoming_phone_number import IncomingPhoneNumberInstance
from twilio.rest.fax.v1.fax import FaxInstance
from twilio.base.exceptions import TwilioRestException
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.fax_response import FaxResponse
from sqlalchemy_utils import PhoneNumber
import unittest
from unittest.mock import patch

from gvo.models.twilio import Twilio
from gvo.models.fax_message import FaxMessage
from test.mocks.request_mock import RequestMock

twilio = Twilio()

error_messages = {"UNAVAILABLE_PHONE": "Unable to create record: +15005550000 is not available",
                  "EMPTY_SMS": "Unable to create record: Message body is required.",
                  "NON_MOBILE": "Unable to create record: To number: +15005550009, is not a mobile number"}

error_uri = {"PHONE": "/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/IncomingPhoneNumbers.json",
             "SMS": "/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages.json"}


def success_twilio_response(class_instance, payload):
    return class_instance(version="2010-04-01",
                          account_sid="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                          payload=payload)


def define_error(status_code, uri, message):
    return TwilioRestException(status=status_code, uri=uri, msg=message)


class TestBuyingPhoneMethod(unittest.TestCase):
    @patch('gvo.models.twilio.Client.incoming_phone_numbers')
    def test_success_phone_number(self, mock):
        phone = PhoneNumber("+15005550006")
        mock.create.return_value = success_twilio_response(IncomingPhoneNumberInstance, {"phone_number": phone.e164})
        response = twilio.buy_phone_number(phone, "voice")
        self.assertEqual(response.phone_number, phone.e164)

    @patch('gvo.models.twilio.Client.incoming_phone_numbers')
    def test_error_unavailable_phone_number(self, mock):
        phone = PhoneNumber("+15005550000")
        mock.create.side_effect = define_error(400, error_uri["PHONE"], error_messages["UNAVAILABLE_PHONE"])
        with self.assertRaises(TwilioRestException) as error:
            twilio.buy_phone_number(phone, "voice")
        self.assertEqual(error.exception.msg, error_messages["UNAVAILABLE_PHONE"])
        self.assertEqual(error.exception.uri, error_uri["PHONE"])


class TestSmsMethod(unittest.TestCase):
    @patch('gvo.models.twilio.Client.messages')
    def test_success_send_sms(self, mock):
        origin_phone = PhoneNumber("+15005550006")
        destination_phone = PhoneNumber("+5571981265131")
        sms = "Sending my test message"
        mock.create.return_value = success_twilio_response(MessageInstance, {"body": sms, "status": "sent"})
        response = twilio.send_sms(origin_phone, destination_phone, sms)
        self.assertEqual(response.body, sms)
        self.assertIn(response.status, ["sent", "queued"])

    @patch('gvo.models.twilio.Client.messages')
    def test_error_sms_with_no_body(self, mock):
        origin_phone = PhoneNumber("+15005550006")
        destination_phone = PhoneNumber("+5571981265131")
        sms = ""
        mock.create.side_effect = define_error(400, error_uri["SMS"], error_messages["EMPTY_SMS"])
        with self.assertRaises(TwilioRestException) as error:
            twilio.send_sms(origin_phone, destination_phone, sms)
        self.assertEqual(error.exception.msg, error_messages["EMPTY_SMS"])
        self.assertEqual(error.exception.uri, error_uri["SMS"])

    @patch('gvo.models.twilio.Client.messages')
    def test_error_sms_non_mobile_number(self, mock):
        origin_phone = PhoneNumber("+15005550006")
        destination_phone = PhoneNumber("+15005550009")
        sms = "Sending my test message"
        mock.create.side_effect = define_error(400, error_uri["SMS"], error_messages["NON_MOBILE"])
        with self.assertRaises(TwilioRestException) as error:
            twilio.send_sms(origin_phone, destination_phone, sms)
        self.assertEqual(error.exception.msg, error_messages["NON_MOBILE"])
        self.assertEqual(error.exception.uri, error_uri["SMS"])


class TestFaxMethod(unittest.TestCase):
    @patch('gvo.models.twilio.Client.fax')
    def test_success_send_fax(self, mock):
        url = "https://www.twilio.com/docs/documents/25/justthefaxmaam.pdf"
        fax_message = FaxMessage(PhoneNumber("+15017122661"), PhoneNumber("+15558675310"), url)
        final_url = "https://fax.twilio.com/v1/Faxes/FXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        mock.faxes.create.return_value = FaxInstance(version="v1", payload={"url": final_url, "status": "sent"})
        response = twilio.send_fax(fax_message)
        self.assertEqual(response.url, final_url)
        self.assertIn(response.status, ["sent", "queued"])

    def test_receive_fax(self):
        origin = PhoneNumber("+15017122661")
        destination = PhoneNumber("+15558675310")
        url = "https://www.twilio.com/docs/documents/25/justthefaxmaam.pdf"
        request = RequestMock(origin.e164, destination.e164, url)
        fax = twilio.receive_fax(request)
        self.assertEqual(fax.origin_phone, origin)
        self.assertEqual(fax.destination_phone, destination)
        self.assertEqual(fax.file_url, url)

    def test_accept_fax(self):
        base_url = os.getenv("BASE_URL")
        url = "fax/received"
        result = FaxResponse()
        result.receive(action=base_url + url)
        self.assertEqual(str(result), twilio.accept_fax(url))

    def test_reject_fax(self):
        result = VoiceResponse()
        result.reject()
        self.assertEqual(str(result), twilio.reject_fax())


class TestCallForwardMethod(unittest.TestCase):
    def test_start_call_forward(self):
        phone = PhoneNumber("+15017122661")
        base_url = os.getenv("BASE_URL")
        extension_url = 'calls/start-forward-call'
        result = VoiceResponse()
        result.dial(number=phone.e164, action=base_url + extension_url)
        self.assertEqual(str(result), twilio.start_call_forward(phone, extension_url))

    def test_end_call_forward_call_completed(self):
        status = "completed"
        extension_url = 'calls/start-forward-call'
        result = VoiceResponse()
        result.hangup()
        self.assertEqual(str(result), twilio.end_call_forward(status, extension_url))

    def test_end_call_forward_call_completed(self):
        status = "failed"
        base_url = os.getenv("BASE_URL")
        extension_url = 'calls/start-forward-call'
        result = VoiceResponse()
        result.say("Please leave a message at the beep. Press the star key when finished.")
        result.record(max_length="30", action=base_url + extension_url)
        result.hangup()
        self.assertEqual(str(result), twilio.end_call_forward(status, extension_url))
