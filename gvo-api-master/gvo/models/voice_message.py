from gvo.models.attachable_message import AttachableMessage


class VoiceMessage(AttachableMessage):
    def __init__(self, origin_phone, destination_phone, url):
        super().__init__(origin_phone, destination_phone, url, 'voice mail')
