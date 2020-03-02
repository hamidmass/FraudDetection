class GvoApiError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        self.status_code = 404


class NonExistentPhoneError(GvoApiError):
    def __init__(self, *args, **kwargs):
        GvoApiError.__init__(self, *args, **kwargs)
        self.args += ("The phone number does not exists", )


class NonFaxPhoneError(GvoApiError):
    def __init__(self, *args, **kwargs):
        GvoApiError.__init__(self, *args, **kwargs)
        self.args += ("The phone number is not a fax number", )


class InvalidPhoneTypeError(GvoApiError):
    def __init__(self, *args, **kwargs):
        GvoApiError.__init__(self, *args, **kwargs)
        self.args += ("The phone type should be fax or voice", )


class NonUserPhoneError(GvoApiError):
    def __init__(self, *args, **kwargs):
        GvoApiError.__init__(self, *args, **kwargs)
        self.args += ("The phone number does not exists", )


class EmptyFaxError(GvoApiError):
    def __init__(self, *args, **kwargs):
        GvoApiError.__init__(self, *args, **kwargs)
        self.args += ("The fax should have content", )


class EmptySmsError(GvoApiError):
    def __init__(self, *args, **kwargs):
        GvoApiError.__init__(self, *args, **kwargs)
        self.args += ("The sms should have content", )


class InvalidPhoneNumberError(GvoApiError):
    def __init__(self, *args, **kwargs):
        GvoApiError.__init__(self, *args, **kwargs)
        self.args += ("The phone format is incorrect. You must use the e164 format", )
