class APPException(Exception):
    status_code = 500

    def __init__(self, message=None):
        Exception.__init__(self)
        if message:
            self.message = message


    def to_dict(self):
        return {
            "status_code": self.status_code,
            "message": self.message
        }


class Unauthorized(APPException):
    status_code = 401
    message = "Not authorized for this action"


class AuthenticationRequired(APPException):
    status_code = 403
    message = "Authentication needed"

