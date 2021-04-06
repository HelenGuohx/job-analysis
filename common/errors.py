class BaseError(Exception):
    def __init__(self, msg=None):
        self.message = msg


class RequestFailureError(BaseError):
    pass

class HTMLElementNotFoundError(BaseError):
    pass
