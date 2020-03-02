class AttachableMessage:
    def __init__(self, origin_phone, destination_phone, url, file_type):
        self.origin_phone = origin_phone
        self.destination_phone = destination_phone
        self.file_url = url
        self.type = file_type
