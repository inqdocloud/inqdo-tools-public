"""
Organizations client
====================
"""

import boto3

from inqdo_tools.utils.error import ErrorHandler


# TODO change return types to list instead of dict
class OrganizationClient(object):
    """This object will construct an Organizations client which takes an
    optional :class:`region name` parameter.
    It will return a dict with a success message/error message or a data set.

    :param region_name: An optional :class:`region_name` argument, which will determine
        the region to which the Organizations client will connect. If none is given it will
        revert to the default, which is eu-west-1.
    :type region_name: str, optional

    :rtype: None
    """

    def __init__(self, **kwargs):
        """Constructor method"""

        # Default region
        self.region_name = "eu-west-1"

        if len(kwargs.items()) > 0:
            for key, value in kwargs.items():
                if key == "region_name":
                    self.region_name = value

        self.organizations = boto3.client("organizations", region_name=self.region_name)

    @ErrorHandler.base_exception
    def get_policy_id(
        self,
        policy_name: str,
    ) -> str:
        """Return the ID of the policy whose name is `policy_name` or return empty string ''
            if policy by that name does not exist.
            Note: also considers policies other than Service Control Policies.

        :param policy_name: This is a string representing a policy name.
        :type policy_name: str

        :rtype: str
        """

        response = self.organizations.list_policies()
        policies = response["policies"]

        policy_id = ""

        policies = filter(lambda el: el["Name"] == policy_name, policies)
        if policies:
            policy_id = policies[0]["Id"]

        return policy_id

    @ErrorHandler.base_exception
    def create_policy(
        self,
        content: str,
        description: str,
        name: str,
        policy_type="SERVICE_CONTROL_POLICY",
    ) -> str:
        """Create a policy in this organization. Return ID upon completion.
            Return dict with error message in case of exception.

        :param content: This is a string which specifies the policy body.
        :type content: str

        :param description: This is a string describing what the policy's purpose is.
        :type description: str

        :param name: Name of the policy.
        :type name: str

        :param policy_type: What type of policy this is. If not passed, by default
            `SERVICE_CONTROL_POLICY`.
        :type policy_type: str

        :rtype: str
        """

        response = self.organizations.create_policy(
            Content=content,
            Description=description,
            Name=name,
            Type=policy_type,
        )

        return response["Policy"]["PolicySummary"]["Id"]

    @ErrorHandler.base_exception
    def attach_policy(self, policy_id: str, target_id) -> dict:
        """Attach policy to target.
            Target can be Root, Account or Organizational Unit identifier.
            Return dict with error message in case of exception or dict with success message.

        :param policy_id: This string specifies the policy identifier.
        :type policy_id: str

        :param target_id: This string specifies the policy identifier.
        :type target_id: str

        :rtype: dict
        """

        self.organizations.attach_policy(
            PolicyId=policy_id,
            TargetId=target_id,
        )
        data = {"Success": "Attached policy."}

        return data

    @ErrorHandler.base_exception
    def delete_policy(self, policy_id: str) -> dict:
        """Delete a policy.

        :param policy_id: This is a string identifier of the policy you want to remove.
        :type policy_id: str

        :rtype: dict
        """

        self.organizations.delete_policy(PolicyId=policy_id)
        data = {"Success": "Deleted policy."}

        return data

    @ErrorHandler.base_exception
    def detach_policy(self, policy_id: str, target_id) -> dict:
        """Detach policy from target.
            Target can be Root, Account or Organizational Unit identifier.
            Return dict with error message in case of exception or dict with success message.

        :param policy_id: This string specifies the policy identifier.
        :type policy_id: str

        :param target_id: This string specifies the target identifier.
        :type target_id: str

        :rtype: dict
        """

        self.organizations.detach_policy(
            PolicyId=policy_id,
            TargetId=target_id,
        )
        data = {"Success": "Attached policy."}

        return data

    @ErrorHandler.base_exception
    def policies_get_all(self) -> list:
        """Retrieves a list of all policies within an organization.
        By default only Service Control Polices are returned,
            excluding other types of policies.

        :rtype: list
        """

        response = self.organizations.list_policies()
        return response["Policies"]

    @ErrorHandler.base_exception
    def get_root_ids(self) -> list:
        """Retrieves a list of all IDs of roots within an organization.
        Upon exception return dict with explanatory error message.

        :rtype: list
        """
        roots = self.organizations.list_roots()["Roots"]
        ids = list(map(lambda el: el["Id"], roots))
        return ids

    def raw_method(self):
        """If you want to run a Organizations operation that isn't currently
        covered by any of the integrated methods of the OrganizationsClient.

        This will return the Organizations connection.

        **NOTE**: This is a quick and dirty solution and usage of this in production
        is discouraged. If you need a new method and it isn't in the library yet,
        add it to this client first, write unit tests, make a PR
        and then use it in your project. This way the library will continue to
        grow and InQdo can garantuee her high quality software deliverance.

        :rtype: Organizations Connection
        """
        return self.organizations
