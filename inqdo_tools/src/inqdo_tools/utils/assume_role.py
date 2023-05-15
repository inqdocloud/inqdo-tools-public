"""
AssumeRole object
=================
"""

import os

import boto3

if "DEBUG_INQDO_TOOLS" in os.environ.keys():  # pragma: no cover
    from utils.common import destruct_dict
else:
    from inqdo_tools.utils.common import destruct_dict


class AssumeRole(object):
    """
    The AssumeRole class is used to obtain temporary security credentials for accessing AWS resources.
    These credentials consist of an access key ID, a secret access key, and a security token.

    The class takes in a role_arn argument, which is the ARN of the role to be assumed,
    and an optional role_session_name argument, which is used as an identifier for the assumed role session.

    It also has a get_credentials method which returns the obtained credentials.

    The class uses the boto3 library to interact with the AWS Security Token Service (STS)
    and make the assume_role API call,
    it also takes in region as a keyword argument which defaults to eu-west-1 if not provided

    :param role_arn: The ARN of the role to be assumed.
    :type role_arn: str

    :param role_session_name: An optional identifier for the assumed role session.
    :type role_session_name: str, optional

    :param region: The region in which to make the API call, defaults to eu-west-1
    :type region: str, optional

    :rtype: dict
    """

    def __init__(self, role_arn: str, **kwargs):
        """Constructor method"""

        destructed_kwargs = None
        self.region = kwargs["region"] if "region" in kwargs else "eu-west-1"

        if "role_session_name" in kwargs:
            destructed_kwargs = destruct_dict(
                dict_to_destruct=kwargs,
                keys=["role_session_name"],
            )

        role_session_name = destructed_kwargs

        self.role_session_name = (
            role_session_name if role_session_name else "AssumeRoleSession"
        )
        self.role_arn = role_arn

        self.sts_client = boto3.client(
            "sts",
            region_name=self.region,
        )

        self.assumed_role_object = self.sts_client.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=self.role_session_name,
        )

        self.credentials = self.assumed_role_object["Credentials"]

    def get_credentials(self) -> dict:
        return self.credentials
