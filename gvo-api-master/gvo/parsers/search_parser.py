class SearchParser:
    def __init__(self, request):
        self.country_code = request.args.get("country_code")
        self.fax_enabled = request.args.get("fax_enabled")
        self.sms_enabled = request.args.get("sms_enabled")
        self.voice_enabled = request.args.get("voice_enabled")
        self.type = request.args.get("type")
