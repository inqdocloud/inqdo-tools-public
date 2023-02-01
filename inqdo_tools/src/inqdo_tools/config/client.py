"""
Config client
=============
"""

import boto3

from inqdo_tools.utils.error import ErrorHandler


class ConfigClient(object):
    """This object will construct a Config client it takes an optional :class:`region name` parameter.
    It will return a dict with a success message/error message or a data set.

    :param region_name: An optional :class:`region_name` argument, which will determine
    the region to which the Cognito client will connect. If none is given it will
    revert to the default, which is eu-west-1.
    :type region_name: str, optional

    :rtype: dict
    """

    def __init__(self, **kwargs):
        """Constructor method"""

        # Default region
        self.region_name = "eu-west-1"

        if len(kwargs.items()) > 0:
            for key, value in kwargs.items():
                if key == "region_name":
                    self.region_name = value

        self.config = boto3.client("config", region_name=self.region_name)

    @ErrorHandler.base_exception
    def organization_create_and_update_managed_rule(
        self,
        config_rule_name: str,
        meta_data: dict,
        excluded_accounts: bool,
    ) -> dict:
        """Apply or update a managed Config rule within an organization.

        :param config_rule_name: This is a string which is the managed config rule you want
            to apply.
        :type config_rule_name: str

        :param meta_data: This is a dictionary with the meta data of the managed config rule
            that you want to apply.
        :type meta_data: dict

        :rtype: dict
        """

        if excluded_accounts:
            self.config.put_organization_config_rule(
                OrganizationConfigRuleName=config_rule_name,
                OrganizationManagedRuleMetadata=meta_data,
                ExcludedAccounts=excluded_accounts,
            )
        else:
            self.config.put_organization_config_rule(
                OrganizationConfigRuleName=config_rule_name,
                OrganizationManagedRuleMetadata=meta_data,
            )

        data = {"Success": "Applied managed config rule."}

        return data

    @ErrorHandler.base_exception
    def organization_create_and_update_custom_rule(
        self, config_rule_name: str, meta_data: dict, excluded_accounts: bool
    ) -> dict:
        """Apply or update a custom Config rule within an organization.

        :param config_rule_name: This is a string which is the managed config rule you want
            to apply.
        :type config_rule_name: str

        :param meta_data: This is a dictionary with the meta data of the managed config rule
            that you want to apply.
        :type meta_data: dict

        :rtype: dict
        """

        if excluded_accounts:
            self.config.put_organization_config_rule(
                OrganizationConfigRuleName=config_rule_name,
                OrganizationCustomRuleMetadata=meta_data,
                ExcludedAccounts=excluded_accounts,
            )
        else:
            self.config.put_organization_config_rule(
                OrganizationConfigRuleName=config_rule_name,
                OrganizationCustomRuleMetadata=meta_data,
            )
        data = {"Success": "Applied custom config rule."}

        return data

    @ErrorHandler.base_exception
    def organization_delete_rule(self, config_rule_name: str) -> dict:
        """Delete a Config rule.

        :param config_rule_name: This is a string which is the managed config rule you want
            to apply.
        :type config_rule_name: str

        :rtype: dict
        """

        self.config.delete_organization_config_rule(
            OrganizationConfigRuleName=config_rule_name
        )
        data = {"Success": "Deleted config rule."}

        return data

    @ErrorHandler.base_exception
    def organization_rule_get_status(self, config_rule_name: str) -> dict:
        """Get the status of a specific Config rule.

        :param config_rule_name: This is a string which is the managed config rule you want
            to apply.
        :type config_rule_name: str

        :rtype: dict
        """

        response = self.config.get_organization_config_rule_detailed_status(
            OrganizationConfigRuleName=config_rule_name
        )
        return response["OrganizationConfigRuleDetailedStatus"]

    @ErrorHandler.base_exception
    def organization_rule_get_status_all(self) -> dict:
        """Retrieves a list of the statuses of all Config rules within an organization.

        :rtype: dict
        """

        response = self.config.describe_organization_config_rule_statuses()
        return response["OrganizationConfigRuleStatuses"]

    @ErrorHandler.base_exception
    def organization_rule_get_all(self) -> dict:
        """Retrieves a list of all Config rules within an organization.

        :rtype: dict
        """

        response = self.config.describe_organization_config_rules()
        return response["OrganizationConfigRules"]
