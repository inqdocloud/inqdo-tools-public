import os

import boto3
import pytest
from moto import mock_sts

from .mocks.cognito import *  # noqa F403
from .mocks.dynamodb import *  # noqa F403
from .mocks.s3 import *  # noqa F403


@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


# STS
@pytest.fixture
def sts_client(aws_credentials):
    with mock_sts():
        conn = boto3.client("sts", region_name="eu-west-1")
        yield conn


# ----
