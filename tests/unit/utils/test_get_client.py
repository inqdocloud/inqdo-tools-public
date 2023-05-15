from inqdo_tools.utils.get_client import Client


def test_client_with_arn(sts_client):
    """Test get client with arn"""

    role_arn = "1234567891010987654321"
    my_client = Client('sts', arn=role_arn)

    assert my_client.region == "eu-west-1"
