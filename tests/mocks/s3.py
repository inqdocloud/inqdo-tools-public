import json
import tempfile

import boto3
import pytest
from moto import mock_s3


@pytest.fixture()
def s3_client(aws_credentials):
    with mock_s3():
        conn = boto3.resource("s3")
        yield conn


@pytest.fixture
def s3_create_bucket(s3_client):
    s3_client.create_bucket(Bucket="s3-test")


@pytest.fixture
def s3_put_object_json(s3_client, s3_create_bucket):

    test = json.dumps({"test": "abc"})

    s3_client.Object("s3-test", "test-file.json").put(Body=test)


@pytest.fixture
def s3_put_object_txt(s3_client, s3_create_bucket):

    content = "test content"
    s3_client.Object("s3-test", "test-file.txt").put(Body=content)
