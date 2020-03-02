import enum


class ServiceNameEnum(enum.Enum):
    fax_send = 1
    fax_receive = 2
    outbound_call = 3
    voice_mail_to_email = 4
    sms = 5

