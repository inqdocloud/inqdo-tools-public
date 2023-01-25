from inqdo_tools.utils.assume_role import AssumeRole


def test_get_credentials(sts_client):
    """Test the AssumeRole object"""

    role_arn = "1234567891010987654321"
    my_client = AssumeRole(
        role_arn=role_arn,
    )

    assert list(my_client.get_credentials().keys()) == [
        "AccessKeyId",
        "SecretAccessKey",
        "SessionToken",
        "Expiration",
    ]


def test_get_credentials_with_session_name(sts_client):
    """Test the AssumeRole object"""

    role_arn = "1234567891010987654321"
    my_client = AssumeRole(
        role_arn=role_arn,
        role_session_name="test_session_name",
    )

    assert list(my_client.get_credentials().keys()) == [
        "AccessKeyId",
        "SecretAccessKey",
        "SessionToken",
        "Expiration",
    ]
