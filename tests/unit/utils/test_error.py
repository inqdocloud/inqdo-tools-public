import boto3
from botocore.exceptions import NoRegionError, ParamValidationError

from inqdo_tools.utils.error import ErrorHandler


class ErrorHandlerTest(object):
    handler = ErrorHandler()

    @ErrorHandler.base_exception
    def test_base_exception_key_error(self):
        test = {"ab": "123"}

        test["123"]

    @ErrorHandler.base_exception
    def test_base_exception_no_region_error(self):
        test_db = boto3.client("dynamodb")
        test_db.put_item()

    @ErrorHandler.base_exception
    def test_base_exception_type_error(self):
        boto3.client("dynamodb", region="eu-west-1")

    @ErrorHandler.base_exception
    def test_base_exception_param_validation_error(self):
        test_db = boto3.client("dynamodb", region_name="eu-west-1")
        test_db.put_item()

    @ErrorHandler.base_exception
    def test_base_exception_error(self):
        a = b  # noqa


def test_key_error_handler():
    result = ErrorHandlerTest().test_base_exception_key_error()

    assert isinstance(result["Message"], KeyError)


def test_type_error_client_handler():
    result = ErrorHandlerTest().test_base_exception_type_error()

    assert isinstance(result["Message"], TypeError)


def test_no_region_error_handler():
    result = ErrorHandlerTest().test_base_exception_no_region_error()

    assert isinstance(result["Message"], NoRegionError)


def test_param_validation_error_handler():
    result = ErrorHandlerTest().test_base_exception_param_validation_error()

    assert isinstance(result["Message"], ParamValidationError)


def test_param_exception_error_handler():
    result = ErrorHandlerTest().test_base_exception_error()

    assert result["Error"] == "Something went wrong."
