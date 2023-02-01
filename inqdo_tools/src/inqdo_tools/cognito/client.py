"""
Cognito client
===============
"""

import os

import boto3

if "DEBUG_INQDO_TOOLS" in os.environ.keys():
    from utils.error import ErrorHandler
else:
    from inqdo_tools.utils.error import ErrorHandler


class CognitoClient(object):
    """
    Constructs a Cognito client, given a user pool ID and an optional region name.
    Returns a dictionary with a success message, error message, or data set.

    :param user_pool_id: ID of the user pool to connect to.
    :type user_pool_id: str

    :param region_name: Region to connect to, defaults to 'eu-west-1' if not provided.
    :type region_name: str, optional

    :return: Dictionary containing success/error message or data set.
    :rtype: dict
    """

    def __init__(self, user_pool_id: str, **kwargs):
        """Constructor method"""

        # Default region
        self.region_name = "eu-west-1"

        if len(kwargs.items()) > 0:
            for key, value in kwargs.items():
                if key == "region_name":
                    self.region_name = value

        # Test if user pool exists, otherwise throw a value error
        user_pool_exists = boto3.client("cognito-idp", region_name=self.region_name)
        try:
            user_pool_exists.describe_user_pool(UserPoolId=user_pool_id)
        except user_pool_exists.exceptions.ResourceNotFoundException:
            raise ValueError(
                f"User pool: '{user_pool_id}' does not exist. Did you create one yet and are you in the correct region?"
            )

        self.cognito = boto3.client("cognito-idp", region_name=self.region_name)
        self.user_pool_id = user_pool_id

    @ErrorHandler.base_exception
    def resend_confirmation_code(self, username: str) -> dict:
        """
        Resends a confirmation code to a user.

        :param username: The username of the user who needs the confirmation.
        :type username: str

        :return: Dictionary with the result of the operation.
        :rtype: dict
        """
        self.cognito.admin_create_user(
            UserPoolId=self.user_pool_id,
            Username=username,
            MessageAction="RESEND",
            DesiredDeliveryMediums=["EMAIL"],
        )

        data = {"Success": "Resend mail"}

        return data

    @ErrorHandler.base_exception
    def disable_enable_user(self, username: str, disable: bool) -> dict:
        """
        Enables or disables a user.

        :param username: The user to be enabled or disabled.
        :type username: str

        :param disable: Flag to determine whether to disable or enable the user.
        :type disable: bool

        :return: Dictionary with the result of the operation.
        :rtype: dict
        """
        if disable:
            self.cognito.admin_disable_user(
                UserPoolId=self.user_pool_id,
                Username=username,
            )
        else:
            self.cognito.admin_enable_user(
                UserPoolId=self.user_pool_id,
                Username=username,
            )

        data = {"Success": "Saved user status."}

        return data

    @ErrorHandler.base_exception
    def update_user_attributes(self, username: str, attributes: list) -> dict:
        """
        Updates the attributes of a specified user.

        :param username: The username of the user to update.
        :type username: str

        :param attributes: List of attributes to update.
        :type attributes: list

        :return: Dictionary with the result of the operation.
        :rtype: dict
        """
        self.cognito.admin_update_user_attributes(
            UserPoolId=self.user_pool_id,
            Username=username,
            UserAttributes=attributes,
        )

        data = {"Success": "Saved user attributes."}

        return data

    @ErrorHandler.base_exception
    def user_create(self, username: str, temporary_password: str, attributes: list) -> dict:
        """
        Creates a new user.

        :param username: The username of the user to create.
        :type username: str

        :param temporary_password: A temporary password for the user.
        :type temporary_password: str

        :return: Dictionary with the result of the operation.
        :rtype: dict
        """
        self.cognito.admin_create_user(
            UserPoolId=self.user_pool_id,
            Username=username,
            TemporaryPassword=temporary_password,
            DesiredDeliveryMediums=["EMAIL"],
            UserAttributes=attributes,
        )
        data = {"Success": "Saved user."}

        return data

    @ErrorHandler.base_exception
    def user_delete(self, username: str) -> dict:
        """
        Deletes a user from Cognito.

        :param username: The username of the user to delete.
        :type username: str

        :return: Dictionary with the result of the operation.
        :rtype: dict
        """
        self.cognito.admin_delete_user(UserPoolId=self.user_pool_id, Username=username)
        data = {"Success": "Deleted user."}

        return data

    @ErrorHandler.base_exception
    def user_get(self, username: str) -> dict:
        """
        Retrieves information about a specific Cognito user.

        :param username: The username of the user to retrieve information for.
        :type username: str

        :return: Dictionary containing user information.
        :rtype: dict
        """
        response = self.cognito.admin_get_user(UserPoolId=self.user_pool_id, Username=username)

        groups = self.cognito.admin_list_groups_for_user(UserPoolId=self.user_pool_id, Username=username)

        groups_list = []
        for group in groups["Groups"]:
            group_name = group["GroupName"]
            groups_list.append(group_name)

        response["Groups"] = groups_list

        return response

    @ErrorHandler.base_exception
    def user_get_all(self) -> dict:
        """
        Retrieves a list of all Cognito users.

        :return: List of users.
        :rtype: list
        """
        r = {"Users": []}
        PaginationToken = None
        while True:
            if PaginationToken:
                response = self.cognito.list_users(UserPoolId=self.user_pool_id, PaginationToken=PaginationToken)
            else:
                response = self.cognito.list_users(
                    UserPoolId=self.user_pool_id,
                )

            for user in response["Users"]:
                r["Users"].append(user)

            if "PaginationToken" in response.keys():
                PaginationToken = response["PaginationToken"]
            else:
                break

        return r["Users"]

    @ErrorHandler.base_exception
    def user_get_all_in_group(self, group_name: str) -> dict:
        """
        Retrieves a list of all Cognito users within a specific group.

        :param group_name: The name of the group to retrieve users from.
        :type group_name: str

        :return: List of users in the specified group.
        :rtype: list
        """
        r = {"Users": []}
        NextToken = None
        while True:
            if NextToken:
                response = self.cognito.list_users_in_group(
                    UserPoolId=self.user_pool_id, GroupName=group_name, NextToken=NextToken
                )
            else:
                response = self.cognito.list_users_in_group(UserPoolId=self.user_pool_id, GroupName=group_name)

            for user in response["Users"]:
                r["Users"].append(user)
            if "NextToken" in response.keys():
                NextToken = response["NextToken"]
            else:
                break

        return r["Users"]

    @ErrorHandler.base_exception
    def user_get_all_with_group(self) -> dict:
        """
        Retrieves a list of all Cognito users, including their group information.

        :param username: The username of the user to retrieve information for.
        :type username: str

        :return: List of users with group information.
        :rtype: list
        """
        r = {"Users": []}
        PaginationToken = None
        while True:
            if PaginationToken:
                response = self.cognito.list_users(UserPoolId=self.user_pool_id, PaginationToken=PaginationToken)
            else:
                response = self.cognito.list_users(
                    UserPoolId=self.user_pool_id,
                )

            for user in response["Users"]:
                groups = self.cognito.admin_list_groups_for_user(
                    UserPoolId=self.user_pool_id, Username=user["Username"]
                )
                groups_list = []
                for group in groups["Groups"]:
                    group_name = group["GroupName"]
                    groups_list.append(group_name)

                user["Groups"] = groups_list
                r["Users"].append(user)

            if "PaginationToken" in response.keys():
                PaginationToken = response["PaginationToken"]
            else:
                break

        return r["Users"]

    @ErrorHandler.base_exception
    def group_create(self, group_name: str) -> dict:
        """
        Creates a new Cognito group.

        :param group_name: The name of the group to create.
        :type group_name: str

        :return: Dictionary with the result of the operation.
        :rtype: dict
        """
        self.cognito.create_group(UserPoolId=self.user_pool_id, GroupName=group_name)
        data = {"Success": "Created group."}

        return data

    @ErrorHandler.base_exception
    def group_get(self, group_name: str) -> dict:
        """
        Retrieves information about a specific Cognito group.

        :param group_name: The name of the group to retrieve information for.
        :type group_name: str

        :return: Dictionary containing group information.
        :rtype: dict
        """
        response = self.cognito.get_group(UserPoolId=self.user_pool_id, GroupName=group_name)

        return response["Group"]

    @ErrorHandler.base_exception
    def group_get_all(self) -> dict:
        """
        Retrieves a list of all Cognito groups.

        :return: Dictionary containing all groups.
        :rtype: dict
        """
        response = self.cognito.list_groups(UserPoolId=self.user_pool_id)

        return response["Groups"]

    @ErrorHandler.base_exception
    def group_delete(self, group_name: str) -> dict:
        """
        Deletes a Cognito group.

        :param group_name: The name of the group to delete.
        :type group_name: str

        :return: Dictionary with the result of the operation.
        :rtype: dict
        """
        self.cognito.delete_group(UserPoolId=self.user_pool_id, GroupName=group_name)
        data = {"Success": "Deleted group."}

        return data

    @ErrorHandler.base_exception
    def group_add_users(self, group_name: str, users: list) -> dict:
        """Add users to Cognito group

        :param group_name: This is a string which is the groupname you want
            to add users to.
        :type group_name: str

        :param users: A list with user names you want to add to the specified
            Cognito group.
        :type users: str

        :rtype: dict
        """

        for user in users:
            self.cognito.admin_add_user_to_group(UserPoolId=self.user_pool_id, GroupName=group_name, Username=user)
        data = {"Success": "Added users to group."}

        return data

    @ErrorHandler.base_exception
    def group_remove_users(self, group_name: str, users: list) -> dict:
        """
        Removes users from a Cognito group.

        :param group_name: The name of the group to remove users from.
        :type group_name: str

        :param users: List of usernames to remove from the group.
        :type users: list

        :return: Dictionary with the result of the operation.
        :rtype: dict
        """
        for user in users:
            self.cognito.admin_remove_user_from_group(UserPoolId=self.user_pool_id, GroupName=group_name, Username=user)
        data = {"Success": "Removed users from group."}

        return data

    @ErrorHandler.base_exception
    def group_add_user_multiple(self, groups: list, username: str) -> dict:
        """
        Puts a given user into multiple Cognito groups at once. Deletes the user from any previous groups.

        :param group_name: The name of the groups to add the user to.
        :type group_name: list

        :param users: The username of the user to add to the groups.
        :type users: str

        :return: Dictionary with the result of the operation.
        :rtype: dict
        """
        current_groups = self.cognito.admin_list_groups_for_user(UserPoolId=self.user_pool_id, Username=username)

        for entry in current_groups["Groups"]:
            self.cognito.admin_remove_user_from_group(
                UserPoolId=self.user_pool_id,
                Username=username,
                GroupName=entry["GroupName"],
            )

        for group in groups:
            self.cognito.admin_add_user_to_group(UserPoolId=self.user_pool_id, GroupName=group, Username=username)

        data = {"Success": "Added user to groups."}

        return data
