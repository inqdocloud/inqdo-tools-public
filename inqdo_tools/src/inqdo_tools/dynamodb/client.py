"""
DynamoDB client
===============
"""

import os
from enum import Enum

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from inqdo_tools.utils.get_client import Client

if "DEBUG_INQDO_TOOLS" in os.environ.keys():
    from utils.common import destruct_dict
    from utils.error import ErrorHandler
else:
    from inqdo_tools.utils.common import destruct_dict
    from inqdo_tools.utils.error import ErrorHandler


class ComparisonOperators(Enum):
    EQ = "EQ"
    LT = "LT"
    NE = "NE"
    LE = "LE"
    GE = "GE"
    GT = "GT"


class DynamoDBClient(object):
    """This object will construct a DynamoDB client which expects the
    :class:`table_name` parameter and takes an optional :class:`region name` parameter.
    It will return a dict with a success message/error message or a data set. Or in
    case of the :class:`raw_method` it will return a DynamoDB Table connection.

    :param table_name: Expects a :class:`table_name` argument which will create
        the appropriate connection to the right table.
    :type table: str

    :param region_name: An optional :class:`region_name` argument, which will determine
        the region to which the DynamoDB client will connect. If none is given it will
        revert to the default, which is eu-west-1.
    :type region_name: str, optional

    :param endpoint_url: An optional :class:`endpoint_url` argument, which will determine
        the endpoint_url for DynamoDB
    :type endpoint_url: str, optional

    :param arn: An optional argument, which will assume the role of the different account to
        which the DynamoDB client will connect.
    :type arn: str, optional

    :rtype: dict
    """

    def __init__(self, table_name: str, **kwargs):
        """Constructor method"""

        # Default region
        self.region_name = "eu-west-1"
        self.endpoint_url = False
        self.arn = False

        if len(kwargs.items()) > 0:
            for key, value in kwargs.items():
                if key == "region_name":
                    self.region_name = value
                if key == "endpoint_url":
                    self.endpoint_url = value
                if key == "arn":
                    self.arn = value

        # Test if table exists, otherwise throw a value error
        test_table_exists = boto3.client("dynamodb", region_name=self.region_name)
        try:
            test_table_exists.describe_table(TableName=table_name)
            self.table_name = table_name
        except test_table_exists.exceptions.ResourceNotFoundException:
            raise ValueError(
                f"Table: '{table_name}' does not exist. Did you create one yet and are you in the correct region?"
            )

        if self.arn:
            self.dynamodb_client = Client("dynamodb", region=self.region_name, arn=self.arn).service

        if self.endpoint_url:
            self.dynamodb = boto3.resource("dynamodb", region_name=self.region_name, endpoint_url=self.endpoint_url)
        else:
            self.dynamodb = boto3.resource("dynamodb", region_name=self.region_name)

        self.table_connection = self.dynamodb.Table(table_name)

    @ErrorHandler.base_exception
    def create_and_update(self, data: dict) -> dict:
        """Create or update a given row in DynamoDB.

        :param data: This takes a :class:`data` argument which needs a primary key - value pair
            that will be used to do create and update operations.
        :type data: dict

        :rtype: dict
        """
        self.table_connection.put_item(Item=data)
        data = {"Success": "Saved or updated item."}

        return data

    @ErrorHandler.base_exception
    def create_and_update_batch(self, batch_list: list) -> dict:
        """Create objects in DynamoDB in batch.

        This expects the :class:`batch_list` parameter.
        It will return an dict with either a success or error message.

        :param batch_list: This is a list containing all the objects that need to be written to
            the database in batch. These objects need to be of type dict. Each object in the
            list needs to have a primary key - value pair.
        :type batch_list: list

        :rtype: dict
        """
        with self.table_connection.batch_writer() as batch:
            for entry in batch_list:
                batch.put_item(Item=entry)

        data = {"Success": "Saved or updated items in batch."}

        return data

    @ErrorHandler.base_exception
    def update(
        self,
        table_primary_key: str,
        value_primary_key: str,
        update_expression: str,
        expression_values: dict,
    ) -> dict:
        """Update single attributes of a DynamoDB row

        :param table_primary_key: The primary key of the table you want to read from.
        :type table_primary_key: str

        :param value_primary_key: The the primary key value of the specific object you want to read.
        :type value_primary_key: str

        :param update_expression: The string with the update expression values, the DynamoDB way.
        :type update_expression: str

        :param expression_values: The dict with the mapped expression key value pairs.
        :type expression_values: dict

        :rtype: dict
        """
        self.table_connection.update_item(
            Key={table_primary_key: value_primary_key},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
        )
        data = {"Success": "Updated fields."}

        return data

    @ErrorHandler.base_exception
    def read(self, table_primary_key: str, value_primary_key: str, **kwargs) -> dict:
        """Read a test single object of a given table in DynamoDB.

        This expects the :class:`table_primary_key` and the :class:`value_primary_key` parameters.
        It will return an dict with either a success or error message.

        Optional keys are :class:`table_sort_key` and :class:`value_sort_key` if there is a sort key.

        :param table_primary_key: The primary key of the table you want to read from.
        :type table_primary_key: str

        :param value_primary_key: The the primary key value of the specific object you want to read.
        :type value_primary_key: str

        :param table_sort_key: An optional :class:`table_sort_key` argument.
        :type table_sort_key: str, optinal

        :param value_sort_key: An optional :class:`value_sort_key` argument.
        :type value_sort_key: str, optinal

        :rtype: dict
        """
        query_dict = {table_primary_key: value_primary_key}

        if "table_sort_key" and "value_sort_key" in kwargs:
            table_sort_key, value_sort_key = self._get_sort_key_value_pair(
                kwargs=kwargs
            )
            query_dict[table_sort_key] = value_sort_key

        response = self.table_connection.get_item(Key=query_dict)

        data = (
            response["Item"]
            if "Item" in response
            else f"No items found. Check your request - query: {query_dict}"
        )

        return data

    @ErrorHandler.base_exception
    def delete(self, table_primary_key: str, value_primary_key: str, **kwargs) -> dict:
        """Delete a single object of a given table in DynamoDB.

        This expects the :class:`table_primary_key` parameter.
        It will return a dict with either a success or error message.

        Optinal (kwargs) :class`table_sort_key` and :class`value_sort_key`

        :param `table_primary_key`: The primary key of the table you want to delete from.
        :type `table_primary_key`: str

        :param value_primary_key: The the primary key value of the specific row you want to delete.
        :type value_primary_key: str

        :param `table_sort_key`: The sort key of the table you want to delete from.
        :type `table_sort_key`: str

        :param value_sort_key: The the sort key value of the specific row you want to delete.
        :type value_sort_key: str

        :rtype: dict
        """
        deletion_dict = {table_primary_key: value_primary_key}

        if "table_sort_key" and "value_sort_key" in kwargs:
            table_sort_key, value_sort_key = self._get_sort_key_value_pair(
                kwargs=kwargs
            )
            deletion_dict[table_sort_key] = value_sort_key

        self.table_connection.delete_item(Key=deletion_dict)
        data = {"Success": "Deleted item from database."}

        return data

    @ErrorHandler.base_exception
    def delete_batch(self, table_primary_key: str, batch_list: list) -> dict:
        """Delete objects in DynamoDB in batch.

        This expects the :class:`table_primary_key` and the :class:`batch_list` parameters.
        It will return an dict with either a success or error message.

        :param table_primary_key: The primary key of the table you want to delete from.
        :type table_primary_key: str

        :param batch_list: This is a list containing all the primary key values of the objects
            that need to be deleted from the database in batch. The items in the list need
            to be of type string.
        :type batch_list: list

        :rtype: dict
        """
        with self.table_connection.batch_writer() as batch:
            for entry in batch_list:
                batch.delete_item(Key={table_primary_key: entry})

        data = {"Success": "Deleted items in batch."}

        return data

    @ErrorHandler.base_exception
    def query(self, table_primary_key: str, query_value: str, **kwargs):
        """Query object in database

        :param table_primary_key: Expects the name of the primary key
        :type table_primary_key: str

        :param query_value: Expects a value which is used for the query.
        :type query_value: str

        :param comparison_operator: Expects :class:`ComparisonOperators` to determine the key condition expression
        :type comparison_operator: :class:`ComparisonOperators`, Optional

        :rtype: list
        """
        if kwargs:
            table_sort_key = kwargs["table_sort_key"]
            value_primary_key = kwargs["value_primary_key"]
            comparison_operator = kwargs["comparison_operator"]

            if (self.arn):
                comparison_functions = {
                    ComparisonOperators.EQ: f"{table_primary_key} = {value_primary_key}",
                    ComparisonOperators.LT: f"{table_sort_key} < {query_value}",
                    ComparisonOperators.LE: f"{table_sort_key} <= {query_value}",
                    ComparisonOperators.GE: f"{table_sort_key} >= {query_value}",
                    ComparisonOperators.GT: f"{table_sort_key} > {query_value}",
                }
                response = self.dynamodb_client.query(
                    TableName=self.table_name,
                    KeyConditionExpression=f"{comparison_functions[ComparisonOperators.EQ]} \
                    AND {comparison_functions[comparison_operator]}"
                )["Items"]
                return self._deserialize(response)

            comparison_functions = {
                ComparisonOperators.EQ: Key(f"{table_primary_key}").eq(
                    f"{value_primary_key}"
                ),
                ComparisonOperators.LT: Key(f"{table_sort_key}").lt(f"{query_value}"),
                ComparisonOperators.LE: Key(f"{table_sort_key}").lte(f"{query_value}"),
                ComparisonOperators.GE: Key(f"{table_sort_key}").gte(f"{query_value}"),
                ComparisonOperators.GT: Key(f"{table_sort_key}").gt(f"{query_value}"),
            }
            return self.table_connection.query(
                KeyConditionExpression=comparison_functions[ComparisonOperators.EQ]
                & comparison_functions[comparison_operator],
            )["Items"]

        if (self.arn):
            response = self.dynamodb_client.query(
                TableName=self.table_name,
                ExpressionAttributeValues={
                    f":{table_primary_key}": self._serialize(query_value)
                },
                KeyConditionExpression=f"{table_primary_key} = :{table_primary_key}"
            )["Items"]
            return self._deserialize(response)

        return self.table_connection.query(
            ExpressionAttributeValues={
                f":{table_primary_key}": {"S": f"{query_value}"}
            },
            KeyConditionExpression=Key(f"{table_primary_key}").eq(f"{query_value}"),
        )["Items"]

    @ErrorHandler.base_exception
    def read_all(self) -> list:
        """Read all objects of a given table in DynamoDB.

        No parameters required, just the :class:`table_name` in the constructor method of the DynamoDBClient.
        It will return an list with all the table rows or an error message.

        :rtype: list
        """
        data = []
        last_evaluated_key = None

        while True:
            if last_evaluated_key:
                response = self.table_connection.scan(
                    ExclusiveStartKey=last_evaluated_key
                )
            else:
                response = self.table_connection.scan()

            for item in response["Items"]:
                data.append(item)

            if "LastEvaluatedKey" in response:
                last_evaluated_key = response["LastEvaluatedKey"]
            else:
                break

        return data

    # TODO FIX THIS
    # def local_secondary_index_query(
    #     self,
    #     index_name: str,
    #     table_primary_key: str,
    #     value_primary_key: str,
    #     local_secondary_sort_key: str,
    #     value_local_secondary_sort_key: str,
    #     comparison_operator: ComparisonOperators,
    # ):
    #     """
    #     Uses a local secondary index to query a table.
    #     This expects an :class:`index_name`, :class:`table_primary_key`,
    #     :class:`value_primary_key`, :class:`local_Secondary_sort_key`,
    #     :class:`value_local_secondary_sory_key`,
    #     and a :class:`comparison_operator` parameter.
    #     Use this method when you have a local secondary index on the table setup.

    #     Parameters
    #     ----------

    #         index_name: str
    #             the name of the local secondary index

    #         partition_key: str
    #             the key used in stead of the original sort key
    #         local_Secondary_sory_query: str
    #             the value you are looking for
    #         local_secondary_sort_key: str
    #             the local secondary sort key
    #         partition_value: str
    #             the value of the partition key.
    #         comparison_perator: ComparisonOperators
    #             can compare with comparison operators.

    #                 - ComparisonOperators.EQ = equals
    #                 - ComparisonOperators.LT = less than
    #                 - ComparisonOperators.LE = Less or equal
    #                 - ComparisonOperators.GE = greater than or equal
    #                 - ComparisonOperators.GT = greater than
    #     """

    #     comparison_functions = {
    #         ComparisonOperators.EQ: Key(f"{local_secondary_sort_key}").eq,
    #         ComparisonOperators.LT: Key(f"{local_secondary_sort_key}").lt,
    #         ComparisonOperators.LE: Key(f"{local_secondary_sort_key}").lt,
    #         ComparisonOperators.GE: Key(f"{local_secondary_sort_key}").gte,
    #         ComparisonOperators.GT: Key(f"{local_secondary_sort_key}").gt,
    #     }

    #     data = []
    #     last_evaluated_key = None

    #     while True:
    #         if last_evaluated_key:
    #             response = self.table_connection.query(
    #                 IndexName=index_name,
    #                 ExclusiveStartKey=last_evaluated_key,
    #                 KeyConditionExpression=Key(f"{table_primary_key}").eq(f"{value_primary_key}")
    #                 & comparison_functions[comparison_operator],
    #             )
    #         else:
    #             response = self.table_connection.query(
    #                 IndexName=index_name,
    #                 KeyConditionExpression=Key(f"{table_primary_key}").eq(f"{value_primary_key}")
    #                 & comparison_functions[comparison_operator](value_local_secondary_sort_key),
    #             )

    #         for item in response["Items"]:
    #             data.append(item)

    #         if "LastEvaluatedKey" in response:
    #             last_evaluated_key = response["LastEvaluatedKey"]
    #         else:
    #             break

    #     return data

    @staticmethod
    def _get_sort_key_value_pair(kwargs):
        destructed_kwargs = destruct_dict(
            dict_to_destruct=kwargs,
            keys=[
                "table_sort_key",
                "value_sort_key",
            ],
        )

        return destructed_kwargs

    @staticmethod
    def _serialize(object):
        serializer = TypeSerializer()
        if type(object) is dict:
            return {k: serializer.serialize(v) for k, v in object.items()}
        else:
            return serializer.serialize(object)

    @staticmethod
    def _deserialize(response):
        deserializer = TypeDeserializer()
        if type(response) is list:
            items = []
            for item in response:
                items.append({k: deserializer.deserialize(v) for k, v in item.items()})
            return items
        elif type(response) is dict:
            return {k: deserializer.deserialize(v) for k, v in response.items()}
        else:
            return deserializer.deserialize(response)

    def get_item(self, key: dict):
        """Get item in database

        :param key: Expects the key of the item to get from the table.
        :type key: dict

        :rtype: dict
        """

        response = self.dynamodb_client.get_item(
            TableName=self.table_name,
            Key=self._serialize(key),
        )["Item"]
        return self._deserialize(response)

    def put_item(self, item: dict):
        """Put item in database

        :param item: Expects the item to add to the table.
        :type item: dict

        :rtype: int
        """

        response = self.dynamodb_client.put_item(
            TableName=self.table_name,
            Item=self._serialize(item)
        )["ResponseMetadata"]["HTTPStatusCode"]

        return response

    def delete_item(self, key: dict):
        """Delete item from database

        :param key: Expects the key of the item to delete from the table.
        :type key: dict

        :rtype: int
        """

        response = self.dynamodb_client.delete_item(
            TableName=self.table_name,
            Key=self._serialize(key)
        )["ResponseMetadata"]["HTTPStatusCode"]

        return response

    def update_item(
        self,
        key: dict,
        expression_attribute_names: dict,
        expression_attribute_values: dict,
        update_expression: str
    ):
        """Update item in database

        :param key: Expects the key of the item to update in the table.
        :type key: dict

        :param expression_attribute_names: Expects one or more substitution tokens for attribute names in an expression.
        :type expression_attribute_names: dict

        :param expression_attribute_values: Expects one or more values that can be substituted in an expression.
        :type expression_attribute_values: dict

        :param update_expression: Expects an expression that defines one or more attributes to be updated, the action
        to be performed on them, and new values for them.
        :type update_expression: dict
        """

        response = self.dynamodb_client.update_item(
            TableName=self.table_name,
            Key=self._serialize(key),
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            UpdateExpression=update_expression,
            ReturnValues="ALL_NEW"
        )["Attributes"]
        return self._deserialize(response)
