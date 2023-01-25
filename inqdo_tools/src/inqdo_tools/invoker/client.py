"""
Invoker object
==============
"""

import json
import logging
import os
import random
import re
import traceback
from datetime import datetime
from typing import Callable

from botocore.exceptions import ClientError

if "DEBUG_INQDO_TOOLS" in os.environ.keys():
    from utils.policy_generator import PolicyGenerator
    from utils.response import Response
else:
    from inqdo_tools.utils.policy_generator import PolicyGenerator
    from inqdo_tools.utils.response import Response


class Invoker(object):
    """
    The Invoker class is used to handle the invocation of a lambda function.

    It takes in event, context and file arguments,
    which are provided by AWS when the lambda is invoked, and a delegate argument,
    which is the function where the rest of the application is invoked.

    It has a set of functions, such as _policy_generator, _logger_name, _config_logging, _handle_error,
    event_body_to_dict etc. which are used to handle the invocation of the lambda function.

    It also uses the logging module for logging and the traceback module for handling errors.

    :param event: The event which the lambda gets from AWS.
    :type event: dict

    :param context: The context from AWS.
    :type context: dict

    :param file: File name file
    :type file: str

    :param delegate: The function where the rest of the application is invoked.
    :type delegate: Callable
    """

    def __init__(self, event: dict, context=dict, file=str, delegate=Callable):
        """Constructor method"""
        self._REGEX_SEPARATOR = re.compile("[/\\\\]")
        self.logger = logging.getLogger(self._logger_name(__file__))

        self.file = file
        self.delegate = delegate
        self.event = event
        self.context = context
        self.body = None

        if "LOG_EVENT" in os.environ:
            if os.environ["LOG_EVENT"] == "true":
                print(self.event)

        self.event_body_to_dict()

    def _policy_generator(func):
        def wrapper(self, **kwargs):
            try:
                if (
                    "GENERATE_POLICY" in os.environ
                    and os.environ["GENERATE_POLICY"] == "true"
                ):
                    policy_gen = PolicyGenerator()
                    policy_gen.record()
                    f = func(self, **kwargs)
                    print(f"\n \n POLICIES: {policy_gen.generate()} \n")
                    return f
                else:
                    return func(self, **kwargs)

            except ClientError as e:
                print(f"Catch in policy generator - {e}")

        return wrapper

    def _logger_name(self, file_name):
        return self._REGEX_SEPARATOR.split(file_name)[-1][:-3]

    def _config_logging(self, file_name):
        formatter = logging.Formatter(
            fmt="{asctime} [{levelname}] '{name}' - {message}",
            style="{",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                handler.setFormatter(formatter)

        inqdo_logger = logging.getLogger(self._logger_name(file_name))
        inqdo_logger.setLevel(logging.INFO)
        return inqdo_logger

    def _handle_error(self):
        trace = traceback.format_exc()
        error_id = "{:%Y-%m-%d %H:%M:%S}-{}".format(
            datetime.now(), random.randint(1000, 9999)
        )

        self.logger.error(
            "An uncaught exception occurred. Error ID %s. Detail %s", error_id, trace
        )

        response = Response(
            body={"Error": 'Oops something went wrong. Error ID "{}"'.format(error_id)},
        )

        return response.error()

    def event_body_to_dict(self):
        """Function to process a Lambda event. This is needed so that every function
            can be used through the Lambda invoke console, as well as through the API
            gateway. This is because through the Lambda invoke console, it will already
            load the json from the body and therefore it would return an error then.
            So we let the error pass silently then.

        :rtype: json
        """
        event_keys = self.event.keys()
        if self.event is not None:
            if "body" in event_keys:
                if self.event["body"] not in ["None", None]:
                    try:
                        loaded_json = json.loads(self.event["body"])
                        if type(loaded_json) == str:
                            self.body = json.loads(loaded_json)
                        else:
                            self.body = loaded_json
                    except Exception:
                        self.body = self.event["body"]
                else:
                    self.body = None
            if "detail" in event_keys:
                try:
                    self.body = self.event["detail"]["body"]
                except KeyError:
                    pass

    @_policy_generator
    def lambda_handler(self):
        logger = self._config_logging(self.file)
        try:
            response = self.delegate(
                event=self.event, body=self.body, context=self.context, logger=logger
            )
        except Exception:
            return self._handle_error()
        return response
