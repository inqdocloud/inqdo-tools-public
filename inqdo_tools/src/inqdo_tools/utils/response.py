"""
Response object
===============
"""
import os

if "DEBUG_INQDO_TOOLS" in os.environ.keys(): # pragma: no cover
    from utils.json import Json
else:
    from inqdo_tools.utils.json import Json


class Response(object):
    """This object will construct a dict with a statusCode, headers and the body. It contains
    multiple methods that can be called which will return the correct response.

    :param body: Expects a :class:`body` argument which will be
        returned as the value of the :class:`body` key in the Response object.
    :type body: dict

    :param headers: An optional :class:`headers` argument which will
        add extra headers to the response. This is completely dynamic and as much headers as required can
        be added.
    :type headers: dict, optional

    :param content_type: An optional :class:`content_type` argument, this should be a string
        with the appropriate name as pre-defined in :class:`self.headers` of the :class:`__init__` method
        of the Response object.
    :type content_type: str, optional

    :rtype: dict
    """

    def __init__(self, body: [dict, str], **kwargs):
        """Constructor method"""
        self.additional_headers = None
        self.response = None
        self.body = Json.compact(body)

        self.content_type = "json"
        self.headers = {
            "json": {
                "Content-Type": "application/json",
            },
            "xml": {
                "Content-Type": "text/xml",
            },
        }

        if len(kwargs.items()) > 0:
            for key, value in kwargs.items():
                if key == "headers":
                    self.additional_headers = value
                if key == "content_type":
                    self.content_type = value

        if self.additional_headers:
            for ctype in ["json", "xml"]:
                self.headers[ctype] = {
                    **self.headers[ctype],
                    **self.additional_headers,
                }

        self.initialize_response()

    def initialize_response(self):
        """Initializes the reponse object"""
        self.response = {
            "statusCode": None,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                **self.headers[self.content_type],
            },
            "body": self.body,
        }

    def ok(self) -> dict:
        """Returns the response with a statuscode 200 OK

        :rtype: dict
        """
        self.response["statusCode"] = 200
        return self.response

    def error(self) -> dict:
        """Returns the response with a statuscode 400 Error

        :rtype: dict
        """
        self.response["statusCode"] = 400
        return self.response

    def unauthorized(self) -> dict:
        """Returns the response with a statuscode 401 Unauthorized

        :rtype: dict
        """
        self.response["statusCode"] = 401
        return self.response

    def forbidden(self) -> dict:
        """Returns the response with a statuscode 403 Forbidden

        :rtype: dict
        """
        self.response["statusCode"] = 403
        return self.response

    def not_found(self) -> dict:
        """Returns the response with a statuscode 404 Not Found

        :rtype: dict
        """
        self.response["statusCode"] = 404
        return self.response

    def conflict(self) -> dict:
        """Returns the response with a statuscode 409 Conflict

        :rtype: dict
        """
        self.response["statusCode"] = 409
        return self.response

    def unprocessable_entity(self) -> dict:
        """Returns the response with a statuscode 422 Unprocessable Entity

        :rtype: dict
        """
        self.response["statusCode"] = 422
        return self.response

    def internal_server_error(self) -> dict:
        """Returns the response with a statuscode 500 Internal server error

        :rtype: dict
        """
        self.response["statusCode"] = 500
        return self.response

    def not_implemented(self) -> dict:
        """Returns the response with a statuscode 501 Not implmented

        :rtype: dict
        """
        self.response["statusCode"] = 501
        return self.response

    def service_unavailable(self) -> dict:
        """Returns the response with a statuscode 503 Service Unavailable

        :rtype: dict
        """
        self.response["statusCode"] = 503
        return self.response
