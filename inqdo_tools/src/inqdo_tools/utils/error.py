"""
Error handler
=============
"""
import inspect
import os

from botocore.exceptions import ClientError, NoRegionError, ParamValidationError

if "DEBUG_INQDO_TOOLS" in os.environ.keys():
    from utils.logger import newline_logger
else:
    from inqdo_tools.utils.logger import newline_logger


class ErrorHandler(object):
    """The common error handler"""

    def base_exception(func):
        """
        A decorator that handles basic (boto) errors. When the decorated function is called,
        it will catch and handle any
        ClientError, KeyError, ParamValidationError, NoRegionError, TypeError and Exception that may occur.
        If the operation is successful and no errors are raised,
        the decorated function will continue to execute as normal.
        """

        def wrapper(*args, **kwargs):
            data = {
                "Error": "Something went wrong.",
            }
            try:
                return func(*args, **kwargs)

            # BOTO - Handle client errors
            except ClientError as e:
                data["Message"] = e.response["Error"]["Message"]
                newline_logger(data, "ERROR")
                return data

            # BOTO - Handle param validation
            except ParamValidationError as e:
                data["Message"] = e
                newline_logger(data, "ERROR")
                return data

            # BOTO - Handle no region error
            except NoRegionError as e:
                data["Message"] = e
                newline_logger(data, "ERROR")
                return data

            # Handle KeyErrors
            except KeyError as e:
                data["Message"] = e
                newline_logger(data, "ERROR")
                return data

            # Handle TypeError
            except TypeError as e:
                data["Message"] = e
                newline_logger(data, "ERROR")
                return data

            # Handle Exception
            except Exception as e:
                data["Message"] = e
                newline_logger(data, "ERROR")
                return data

        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        wrapper.__signature__ = inspect.signature(func)

        return wrapper
