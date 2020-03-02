from gvo.models.attachable_message import AttachableMessage


class FaxMessage(AttachableMessage):
    def __init__(self, origin_phone, destination_phone, url):
        super().__init__(origin_phone, destination_phone, url, 'fax')
