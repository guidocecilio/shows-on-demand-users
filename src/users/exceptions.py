import flask
from flask_restplus import fields, Api, marshal

from users import constants

API = Api()

ERROR_DETAIL_SCHEMA = API.model('ErrorDetailSchema', {
    constants.KEY_FIELD: fields.String(),
    constants.KEY_MESSAGE: fields.String()
})

EXCEPTION_SCHEMA = API.model('ExceptionSchema', {
    constants.KEY_MESSAGE: fields.String(),
    constants.KEY_STATUS: fields.Integer(required=True),
    constants.KEY_CODE: fields.String(required=True),
    constants.KEY_DETAIL: fields.String(),
    constants.KEY_ERRORS: fields.List(
        fields.Nested(ERROR_DETAIL_SCHEMA, allow_null=True, skip_none=True),
        default=None)
})


class APIException(Exception):
    """ Base class for all API specific exceptions.
    Should allow holding all extra attributes that CMC asks in error results. """
    code = 'RUNTIME_API_EXCEPTION'
    message = ""
    errors = None
    http_code = 500

    def __init__(self, detail="", message=None, code=None, errors=None):
        """
        :param detail: Extra information you want to add to the error response in addition to 'message'
        :param message: Overwrite standard message for this error type
        :param code: Overwrite standard code for this request
        :param errors: Any extra errors you want to pass in. Expecting a list of dict(field=, message=) entries
        """
        super().__init__(detail)
        self.detail = detail
        if code:
            self.code = code
        if message:
            self.message = message
        if errors:
            if not isinstance(errors, list):
                raise ValueError("Invalid use of errors. Expecting a list of [dict(field=, message=), .. entries.")
            for error in errors:
                if (not isinstance(error, dict) or
                        constants.KEY_FIELD not in error or
                        constants.KEY_MESSAGE not in error):
                    raise ValueError("Incorrect error {} found. Expecting dict(field=, message=) dictionary".format(
                        error
                    ))
            self.errors = errors

    def to_dict(self):
        error_data = {
            constants.KEY_MESSAGE: self.message,
            constants.KEY_STATUS: self.http_code,
            constants.KEY_CODE: self.code
        }

        if self.detail:
            error_data[constants.KEY_DETAIL] = self.detail

        if self.errors:
            error_data[constants.KEY_ERRORS] = self.errors

        return marshal(error_data, EXCEPTION_SCHEMA, skip_none=True)

    def to_response(self):
        """ Return response in line with CMC requirements. """
        response = flask.jsonify(self.to_dict())
        response.status_code = self.http_code
        return response

    def __str__(self):
        return f'{self.__class__.__name__}(msg={self.message}, status_code={self.code}, detail={self.detail})'


class AuthenticationRequired(APIException):
    http_code = 401
    code = "AUTHENTICATION_REQUIRED"
    message = "No authentication bearer token specified in authorization header."


class NotAuthorized(APIException):
    http_code = 403
    code = "NOT_AUTHORIZED"
    message = "You are not authorized to perform the requested action."


class ResourceNotFound(APIException):
    http_code = 404
    code = "NOT_FOUND"
    message = "The requested resource was not found."


class BadRequest(APIException):
    http_code = 400
    code = "BAD_REQUEST"
    message = "The request could not be understood by the server due to malformed syntax."


class InvalidDate(APIException):
    http_code = 400
    code = "BAD_REQUEST"
    message = "Dates must be specified as ISO-8601 strings. For example: yyyy-MM-ddTHH:mm:ss.SSSZ"


class InvalidValue(APIException):
    http_code = 422
    code = 'INVALID_VALUE'
    message = "Value [{}] is not valid for field type [{}]."

    def __init__(self, invalid_value, value_type, allowed_values=None, **kwargs):
        """
        :param invalid_value: The value for which you need to raise an exception
        :param value_type: The expected type of that value
        :param allowed_values: If you have some enum of allowed types
        :param kwargs: Extra base APIException arguments
        """
        message = self.message.format(invalid_value, value_type)
        if allowed_values:
            message += "Allowable values are: {}".format(allowed_values)
        super().__init__(message=message, **kwargs)


class TooManyRequests(APIException):
    http_code = 429
    code = "TOO_MANY_REQUESTS"
    message = "Rate limit exceeded the maximum [{}] requests within [{}] seconds"

    def __init__(self, max_requests, time_window, **kwargs):
        """
        :param max_requests: The limit that was just reached in term of number of requests
        :param time_limit: The time window over which the limit was reached
        :param kwargs: Extra base APIException arguments
        """
        message = self.message.format(max_requests, time_window)
        super().__init__(message=message, **kwargs)


class ServerError(APIException):
    http_code = 500
    code = "INTERNAL_SERVER_ERROR"
    message = "The server encountered an unexpected condition which prevented it from fulfilling the request."


class MethodNotImplemented(APIException):
    http_code = 501
    code = "NOT_IMPLEMENTED"
    message = "Not Implemented."


class RequestTimeout(APIException):
    http_code = 408
    code = "GATEWAY_TIMEOUT"
    message = "The request timed out."
