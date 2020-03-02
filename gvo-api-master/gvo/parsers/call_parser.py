from sqlalchemy_utils import PhoneNumber


class CallParser:
    def __init__(self, request):
        self.origin_phone = PhoneNumber(request.form.get('From'))
        self.destination_phone = PhoneNumber(request.form.get('To'))
        self.call_status = request.form.get("CallStatus")
