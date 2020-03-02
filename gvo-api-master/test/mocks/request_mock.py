class RequestMock:
    def __init__(self, from_, to_, media_url):
        self.form = {"From": from_,
                     "To": to_,
                     "MediaUrl": media_url}
