class ApiError(Exception):
    status_code = 500
    code = "internal_error"

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class NotFound(ApiError):
    status_code = 404
    code = "not_found"


class Conflict(ApiError):
    status_code = 409
    code = "conflict"


class ValidationFailed(ApiError):
    status_code = 422
    code = "validation_error"
