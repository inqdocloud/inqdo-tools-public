import boto3
import pytest
from moto import mock_ssm


@pytest.fixture()
def ssm_client(aws_credentials):
    with mock_ssm():
        conn = boto3.client('ssm', region_name="eu-west-1")
        yield conn


@pytest.fixture
def ssm_create_parameter(ssm_client):
    ssm_client.put_parameter(
        Name='/root/key1',
        Value='value1',
        Type='String'
    )
