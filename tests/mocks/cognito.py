import boto3
import pytest
from moto import mock_cognitoidp


@pytest.fixture()
def cognito_client(aws_credentials):
    with mock_cognitoidp():
        conn = boto3.client("cognito-idp", region_name="eu-west-1")
        yield conn


@pytest.fixture
def cognito_create_user_pool(cognito_client):
    # Create a mock user pool
    response = cognito_client.create_user_pool(PoolName="my-pool")
    yield response


@pytest.fixture
def cognito_create_user(cognito_client, cognito_create_user_pool):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito_client.admin_create_user(
        UserPoolId=user_pool_id,
        Username="test_user",
        TemporaryPassword="Passw0rd!",
        UserAttributes=[
            {"Name": "email", "Value": "my-user@example.com"},
            {"Name": "email_verified", "Value": "true"},
        ],
    )


@pytest.fixture
def cognito_create_group(cognito_client, cognito_create_user_pool):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito_client.create_group(
        UserPoolId=user_pool_id, GroupName="test_group", Description="Test group"
    )


@pytest.fixture
def cognito_create_multiple_groups(cognito_client, cognito_create_user_pool):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito_client.create_group(
        UserPoolId=user_pool_id, GroupName="test_group_1", Description="Test group 1"
    )
    cognito_client.create_group(
        UserPoolId=user_pool_id, GroupName="test_group_2", Description="Test group 2"
    )
    cognito_client.create_group(
        UserPoolId=user_pool_id, GroupName="test_group_3", Description="Test group 3"
    )


@pytest.fixture
def cognito_create_group_with_user(
    cognito_client, cognito_create_user_pool, cognito_create_user
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito_client.create_group(
        UserPoolId=user_pool_id, GroupName="test_group", Description="Test group"
    )

    cognito_client.admin_add_user_to_group(
        UserPoolId=user_pool_id, GroupName="test_group", Username="test_user"
    )


@pytest.fixture
def cognito_create_users_in_groups(
    cognito_client, cognito_create_user_pool, cognito_create_group
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]

    for user in ["user-1", "user-2"]:
        cognito_client.create_group(
            UserPoolId=user_pool_id,
            GroupName=f"test_group_{user}",
            Description=f"test_group_{user}",
        )
        cognito_client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=user,
            TemporaryPassword="Passw0rd!",
            UserAttributes=[
                {"Name": "email", "Value": f"{user}@example.com"},
                {"Name": "email_verified", "Value": "true"},
            ],
        )

        cognito_client.admin_add_user_to_group(
            UserPoolId=user_pool_id, GroupName="test_group", Username=user
        )
        cognito_client.admin_add_user_to_group(
            UserPoolId=user_pool_id, GroupName=f"test_group_{user}", Username=user
        )


@pytest.fixture
def cognito_create_multiple_users_groups(
    cognito_client, cognito_create_user_pool, cognito_create_group
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]

    for index in range(150):
        cognito_client.create_group(
            UserPoolId=user_pool_id,
            GroupName=f"test_group_{index}",
            Description=f"test_group_{index}",
        )
        cognito_client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=f"user-{index}",
            TemporaryPassword="Passw0rd!",
            UserAttributes=[
                {"Name": "email", "Value": f"{index}@example.com"},
                {"Name": "email_verified", "Value": "true"},
            ],
        )

        cognito_client.admin_add_user_to_group(
            UserPoolId=user_pool_id, GroupName="test_group", Username=f"user-{index}"
        )
        cognito_client.admin_add_user_to_group(
            UserPoolId=user_pool_id, GroupName=f"test_group_{index}", Username=f"user-{index}"
        )
