"""
inQdo Tools library
"""
from __future__ import absolute_import

from ._version import __version__
from .dynamodb.client import DynamoDBClient
from .ec2.client import Ec2
from .events.client import EventsClient
from .invoker.client import Invoker
from .s3.client import S3Client
from .ssm.client import ParameterStore
from .utils.assume_role import AssumeRole
from .utils.common import (
    b64decode,
    b64encode,
    destruct_dict,
    dict_get,
    dict_get_forced,
    dict_set,
    from_json,
    to_json,
)
from .utils.get_client import Client
from .utils.logger import InQdoLogger, newline_logger
from .utils.response import Response

__author__ = "inQdo Cloud (info@inqdo.cloud)"
__license__ = "MIT"
__version__ = __version__

__all__ = (
    "DynamoDBClient",
    "ParameterStore",
    "AssumeRole",
    "Client",
    "Response",
    "destruct_dict",
    "dict_get",
    "dict_get_forced",
    "dict_set",
    "from_json",
    "to_json",
    "b64encode",
    "b64decode",
    "EventsClient",
    "Invoker",
    "InQdoLogger",
    "newline_logger",
    "S3Client",
    "Ec2",
)
