import os
import sys

from dynamodb.client import ComparisonOperators, DynamoDBClient
from invoker.client import Invoker
from ssm.client import ParameterStore
from utils.logger import newline_logger
from utils.response import Response

sys.path.append(os.path.join(os.path.dirname(__file__)))


# FUNCTION TO DELEGATE
def test_parameter_store(event, body, context, logger):

    store = ParameterStore(prefix="/inqdo")
    print(store.keys())
    print(store["asg"]["addns"])


def test(event, body, context, logger):
    table = DynamoDBClient("dynamo-db-secondary-local-test-database-dev")

    r = table.local_secondary_index_query(
        index_name="indexName",
        table_primary_key="Band",
        value_primary_key="Test",
        local_secondary_sort_key="name",
        value_local_secondary_sort_key=20,
        comparison_operator=ComparisonOperators.EQ,
    )
    newline_logger(r, "RESPONSE")

    return Response(body={"ok": 200}).ok()


def handler(event, context):
    Invoker(
        event=event, context=context, file=__file__, delegate=test_parameter_store
    ).lambda_handler()

    return Invoker(
        event=event, context=context, file=__file__, delegate=test
    ).lambda_handler()
