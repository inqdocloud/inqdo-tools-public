"""
Error handler
=============
"""

import inspect

from botocore.exceptions import ClientError, NoRegionError, ParamValidationError


class ErrorHandler(object):
    """The common error handler"""

    def base_exception(func):
        """
        A decorator that handles basic boto errors. When the decorated function is called, it will catch and handle any
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

            # Handle normal boto errors
            except ClientError as e:
                data["Message"] = e.response["Error"]["Message"]
                return data

            # Handle KeyErrors
            except KeyError as e:
                data["Message"] = e
                return data

            # Handle Param validation
            except ParamValidationError as e:
                data["Message"] = e
                return data

            # No region error
            except NoRegionError as e:
                data["Message"] = e
                return data

            # TypeError
            except TypeError as e:
                data["Message"] = e
                return data

            # Exception
            except Exception as e:
                data["Message"] = e
                return data

        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        wrapper.__signature__ = inspect.signature(func)

        return wrapper
