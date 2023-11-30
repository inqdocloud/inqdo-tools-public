import os

if "DEBUG_INQDO_TOOLS" in os.environ.keys():
    from utils.get_client import Client
else:
    from inqdo_tools.utils.get_client import Client


class Ec2(object):
    """This object gets ec2 instances objects from a specific AWS account.
    :param account_info: required param. Keys: arn, region.
    :param instance_ids: specified instance ids for lookup.
    """

    def __init__(self, account_info: dict, instance_ids=[]):
        self.account_info = account_info
        self.instance_ids = instance_ids
        self.ec2 = None

        self.ec2_client = Client(
            service="ec2",
            arn=self.account_info["arn"],
            region=self.account_info["region"],
        ).service

        # DATA KEY VALUES ACCOUNT INFO
        for key in [
            "region",
            "arn",
        ]:
            setattr(self, key, _get_key_value(data=self.account_info, key=key))

        # INSTANCE CODES
        self.status_pending = 0
        self.status_running = 16
        self.status_terminated = 32
        self.status_stopping = 64
        self.status_stopped = 80

    def get_all(self) -> list:
        next_token = None
        all_instances = []

        while True:
            if next_token:
                response = self.ec2_client.describe_instances(
                    InstanceIds=self.instance_ids, NextToken=next_token
                )
            else:
                response = self.ec2_client.describe_instances(
                    InstanceIds=self.instance_ids
                )

            for data in response.get("Reservations", []):
                for ec2_item in data["Instances"]:
                    all_instances.append(
                        Ec2Instance(
                            data=ec2_item,
                            account_info=self.account_info,
                        )
                    )

            if "NextToken" in response:
                next_token = response["NextToken"]
            else:
                break

        return all_instances

    def get_instance(self, instance_id: str):
        response = self.ec2_client.describe_instances(InstanceIds=[instance_id])[
            "Reservations"
        ][0]["Instances"][0]

        return Ec2Instance(data=response, account_info=self.account_info)

    def get_all_instance_ids_in_list(self) -> list:
        return [ec2.instance_id for ec2 in self.get_all()]


class Ec2Instance(Ec2):
    def __init__(self, data: dict, account_info: dict):
        super(Ec2Instance, self).__init__(account_info)
        self.ec2_data = data

        # DATA KEY VALUES
        for key in [
            ("InstanceId", "instance_id"),
            ("State,Name", "status"),
            ("State", "state"),
        ]:
            k, name = key
            setattr(self, name, _get_key_value(data=self.ec2_data, key=k))

        # INITIAL NAME
        self.instance_name = self.instance_id
        self.documents = []
        self._describe_tags()
        self._describe_association()

    # GET TAG BY KEY
    def get_tag_value(self, key: str):
        try:
            tag = [t[key] for t in self.tags if key in t.keys()]

            if len(tag) > 0:
                return tag[0]

            return False
        except Exception:
            return False

    # CREATE TAGS
    def create_tags(self, key: str, value: str):
        try:
            self.ec2_client.create_tags(
                DryRun=False,
                Resources=[
                    self.instance_id,
                ],
                Tags=[{"Key": key, "Value": value}],
            )
        except Exception as e:
            # NEED TO HAVE A ERROR LOGGER
            print(e)

    # DELETE TAGS
    def delete_tags(self, key: str):
        try:
            self.ec2_client.delete_tags(
                Resources=[self.instance_id], Tags=[{"Key": key}]
            )
        except Exception as e:
            # NEED TO HAVE A ERROR LOGGER
            print(e)

    # GET ALL TAGS FROM EC2
    def _describe_tags(self):
        next_token = None
        self.tags = []

        while True:
            if next_token:
                response = self.ec2_client.describe_tags(
                    Filters=[
                        {
                            "Name": "resource-id",
                            "Values": [
                                self.instance_id,
                            ],
                        }
                    ],
                    NextToken=next_token,
                )
            else:
                response = self.ec2_client.describe_tags(
                    Filters=[
                        {
                            "Name": "resource-id",
                            "Values": [
                                self.instance_id,
                            ],
                        }
                    ],
                )

            # GET TAGS FROM RESPONSE
            for tag in response.get("Tags", []):
                key = tag["Key"]
                value = tag["Value"]

                # GET INSTANCE NAME
                if key == "Name":
                    self.instance_name = value

                self.tags.append({key: value})

            if "NextToken" in response:
                next_token = response["NextToken"]
            else:
                break

    # GET ASSOCIATION
    def _describe_association(self) -> dict:
        ssm_client = Client(service="ssm", arn=self.arn, regin=self.region).service

        try:
            response = ssm_client.describe_instance_associations_status(
                InstanceId=self.instance_id
            )["InstanceAssociationStatusInfos"]

            self.documents = [
                association["Name"]
                for association in response
                if "icp-" in association["Name"]
            ]

        except Exception as e:
            print(e)

    def start(self):
        response = self.ec2_client.start_instances(
            InstanceIds=[self.instance_id],
        )
        return response

    def stop(self):
        response = self.ec2_client.stop_instances(
            InstanceIds=[self.instance_id],
        )

        return response


def _get_key_value(data: dict, key: str):
    if "," in key:
        while True:
            v = ""
            obj = {}
            last_key = ""
            for k in key.split(","):
                last_key = k
                if len(obj.keys()) == 0:
                    get = data.get(k, None)
                else:
                    get = obj.get(k, None)
                if isinstance(get, dict):
                    obj = get
                else:
                    v = obj[last_key]
                    return v
    else:
        return data[key]
