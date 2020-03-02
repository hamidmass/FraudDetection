from flask_mail import Mail, Message
from gvo.app import app
import requests

FILE_NAME = {"fax": "fax.pdf", "voice mail": "voicemail.wav"}
CONTENT_TYPE = {"fax": "application/pdf", "voice mail": "audio/wav"}


class MailSender:
    def __init__(self):
        self.mail = Mail(app)
        self.subject = "You received a new {}"
        self.body = "You received a new {} on your number {} from {}."

    def send_email(self, file, destination):
        attach = requests.get(file.file_url)
        message = Message(subject=self.subject.format(file.type),
                          recipients=[destination],
                          body=self.body.format(file.type, file.destination_phone, file.origin_phone))
        message.attach(FILE_NAME[file.type], CONTENT_TYPE[file.type], attach.content)
        self.mail.send(message)
