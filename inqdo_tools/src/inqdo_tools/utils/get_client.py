"""
Client object
===============
"""
import os

import boto3

if "DEBUG_INQDO_TOOLS" in os.environ.keys():  # pragma: no cover
    from .assume_role import AssumeRole
    from .common import destruct_dict
else:
    from .assume_role import AssumeRole
    from .common import destruct_dict


class Client(object):
    """
    The Client class is used to obtain a boto3 client for a specific service.

    It takes in a service argument, which is the name of the service for which the client is required,
    and an optional credentials argument, which is a dict containing the credentials to be used to access
    the client within another account and an optional region argument which is used to
    switch to the desired region, the default region is eu-west-1.

    The class uses the boto3 library to interact with the AWS services,
    it also uses AssumeRole class to obtain the temporary security credentials if arn is provided in the arguments.

    :param service: The name of the service for which the client is required.
    :type service: str

    :param credentials: An optional dict containing the credentials
    to be used to access the client within another account.
    :type credentials: dict, optional

    :param region: The region in which to make the API call, defaults to eu-west-1
    :type region: str, optional

    :rtype: dict
    """

    def __init__(self, service: str, **kwargs):
        """Constructor method"""
        self.service = service
        self.region = kwargs["region"] if "region" in kwargs else "eu-west-1"
        self.get(**kwargs)

    def get(self, **kwargs) -> dict:
        if "arn" in kwargs:
            credentials = AssumeRole(role_arn=kwargs["arn"]).get_credentials()

            destructed_items = destruct_dict(
                dict_to_destruct=credentials,
                keys=[
                    "AccessKeyId",
                    "SecretAccessKey",
                    "SessionToken",
                ],
            )

            access_key_id, secret_access_key, session_token = destructed_items

            self.service = boto3.client(
                self.service,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                aws_session_token=session_token,
                region_name=self.region,
            )
        else:
            self.service = boto3.client(
                self.service,
                region_name=self.region,
            )
