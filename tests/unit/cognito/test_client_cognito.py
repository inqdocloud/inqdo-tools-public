from inqdo_tools.cognito.client import CognitoClient


# CREATE AND UPDATE
def test_create_and_update(
    cognito_client, cognito_create_user_pool, cognito_create_user
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    # Call the resend_confirmation_code method
    result = cognito.resend_confirmation_code("test_user")

    # Assert that the correct data is returned
    assert result == {"Success": "Resend mail"}


# DISABLE/ENABLE USER
def test_disable_enable_user(
    cognito_client, cognito_create_user_pool, cognito_create_user
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.disable_enable_user("test_user", True)

    assert result == {"Success": "Saved user status."}


# UPDATE USER ATTRIBUTES
def test_update_user_attributes(
    cognito_client, cognito_create_user_pool, cognito_create_user
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    # Test for updating user attributes
    result = cognito.update_user_attributes(
        "test_user", [{"Name": "email", "Value": "test_user@example.com"}]
    )

    assert result == {"Success": "Saved user attributes."}


# UPDATE USER ATTRIBUTES ERROR
def test_update_user_attributes_error(
    cognito_client, cognito_create_user_pool, cognito_create_user
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    # Test for updating user attributes
    result = cognito.update_user_attributes(
        "test_user", [{"Nae": "email", "Value": "test_user@example.com"}]
    )

    assert "Error" in result.keys()


# USER CREATE
def test_user_create(cognito_client, cognito_create_user_pool):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    # Arrange
    username = "testuser"
    temporary_password = "Test1234!"
    attributes = [
        {"Name": "email", "Value": "testuser@example.com"},
        {"Name": "given_name", "Value": "Test"},
        {"Name": "family_name", "Value": "User"},
    ]

    # Act
    result = cognito.user_create(username, temporary_password, attributes)

    print(result, "re \n")

    # Assert
    assert result == {"Success": "Saved user."}


# USER CREATE ERROR
def test_user_create_error(cognito_client, cognito_create_user_pool):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    # Arrange
    username = "testuser"
    temporary_password = "Test1234!"
    attributes = [
        {"ame": "email", "Value": "testuser@example.com"},
        {"Name": "given_name", "Value": "Test"},
        {"Name": "family_name", "Value": "User"},
    ]

    # Act
    result = cognito.user_create(username, temporary_password, attributes)

    print(result, "re \n")

    # Assert
    assert "Error" in result.keys()


#  USER DELETE
def test_user_delete(cognito_client, cognito_create_user_pool, cognito_create_user):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    # Arrange
    username = "test_user"
    result = cognito.user_delete(username)
    # Assert
    assert result == {"Success": "Deleted user."}


#  USER GET
def test_user_get(
    cognito_client, cognito_create_user_pool, cognito_create_user, cognito_create_group
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    # Arrange
    username = "test_user"
    result = cognito.user_get(username)

    assert result["Username"] == "test_user"


#  USER GET ALL
def test_user_get_all(
    cognito_client, cognito_create_user_pool, cognito_create_multiple_users_groups,
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.user_get_all()

    filtered_users = [
        {"Username": user["Username"]} for user in result
    ]

    assert len(filtered_users) == 150


#  USER GET ALL IN GROUP
def test_user_get_all_in_group(
    cognito_client, cognito_create_user_pool, cognito_create_multiple_users_groups,
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.user_get_all_in_group(group_name="test_group")

    filtered_users = [
        {"Username": user["Username"]} for user in result
    ]

    assert len(filtered_users) == 150


#  USER GET WITH GROUP INFO
def test_user_get_with_group_info(
    cognito_client,
    cognito_create_user_pool,
    cognito_create_user,
    cognito_create_group_with_user,
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    # Arrange
    username = "test_user"
    result = cognito.user_get(username)

    assert result["Groups"] == ["test_group"]


# USER GET ALL WITH GROUP INFO
def test_user_get_all_with_group_info(
    cognito_client, cognito_create_user_pool, cognito_create_multiple_users_groups
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.user_get_all_with_group()

    filtered_users = [
        {"Username": user["Username"], "Groups": user["Groups"]} for user in result
    ]
    user_groups = {user["Username"]: user["Groups"] for user in result}

    assert len(filtered_users) == 150
    assert "test_group_1" in user_groups["user-1"]
    assert "test_group_2" in user_groups["user-2"]


# GROUP CREATE
def test_group_create(cognito_client, cognito_create_user_pool):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.group_create(group_name="ABC")

    assert result == {"Success": "Created group."}


# GROUP GET
def test_group_get(cognito_client, cognito_create_user_pool, cognito_create_group):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.group_get(group_name="test_group")

    assert result["GroupName"] == "test_group"


# GROUP GET ALL
def test_group_get_all(
    cognito_client, cognito_create_user_pool, cognito_create_multiple_groups
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.group_get_all()

    groups = [group["GroupName"] for group in result]

    assert len(groups) == 3
    assert "test_group_1" in groups
    assert "test_group_2" in groups
    assert "test_group_3" in groups


# GROUP DELETE
def test_group_delete(
    cognito_client, cognito_create_user_pool, cognito_create_multiple_groups
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.group_delete(group_name="test_group_2")

    assert result == {"Success": "Deleted group."}


# GROUP ADD USERS
def test_group_add_users(
    cognito_client, cognito_create_user_pool, cognito_create_users_in_groups
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.group_add_users(
        group_name="test_group", users=["user-1", "user-2"]
    )

    assert result == {"Success": "Added users to group."}


# GROUP REMOVE USERS
def test_group_remove_users(
    cognito_client, cognito_create_user_pool, cognito_create_users_in_groups
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.group_remove_users(
        group_name="test_group", users=["user-1", "user-2"]
    )

    assert result == {"Success": "Removed users from group."}


# GROUP ADD MULTIPLE USERS IN GROUP
def test_group_add_user_multiple(
    cognito_client, cognito_create_user_pool, cognito_create_users_in_groups
):
    user_pool_id = cognito_create_user_pool["UserPool"]["Id"]
    cognito = CognitoClient(user_pool_id=user_pool_id)

    result = cognito.group_add_user_multiple(
        groups=["test_group", "test_group_user-1"], username="user-2"
    )

    assert result == {"Success": "Added user to groups."}
