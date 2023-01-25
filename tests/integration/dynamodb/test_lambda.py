from inqdo_tools.dynamodb.client import DynamoDBClient
from inqdo_tools.utils.common import event_body_to_dict
from inqdo_tools.utils.response import Response


# CERATE AND UPDATE OK
def test_lambda_handler_create_and_update_ok(
    dynamodb_client, dynamodb_create_table, event_create_and_update, context=None
):

    data = event_body_to_dict(event_create_and_update)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.create_and_update(data=data)

    if "Success" in db_response:
        res = Response(body=db_response).ok()
    else:
        res = Response(body=db_response).error()

    assert res == {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"Success": "Saved or updated item."}',
    }


# CREATE AND UPDATE RANGE OK
def test_lambda_handler_create_and_update_range_ok(
    dynamodb_client,
    dynamodb_create_table_with_range_key,
    event_create_and_update_range,
    context=None,
):

    data = event_body_to_dict(event_create_and_update_range)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.create_and_update(data=data)

    if "Success" in db_response:
        res = Response(body=db_response).ok()
    else:
        res = Response(body=db_response).error()

    assert res == {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"Success": "Saved or updated item."}',
    }


# CERATE AND UPDATE MISSING PRIMARY KEY
def test_lambda_handler_create_and_update_error_missing_primary_key(
    dynamodb_client, dynamodb_create_table, event_missing_primary_key, context=None
):
    data = event_body_to_dict(event_missing_primary_key)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.create_and_update(data=data)

    if "Success" in db_response:
        res = Response(body=db_response).ok()
    else:
        res = Response(body=db_response).error()

    assert res == {
        "statusCode": 400,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"Error": "Something went wrong.", "Message": "One or more parameter values were invalid: Missing the key movieName in the item"}',  # noqa: E501
    }


# CREATE AND UPDATE RANGE MISSING KEYS
def test_lambda_handler_create_and_update_range_missing_keys(
    dynamodb_client,
    dynamodb_create_table_with_range_key,
    event_create_and_update_range_missing_keys,
    context=None,
):

    data = event_body_to_dict(event_create_and_update_range_missing_keys)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.create_and_update(data=data)

    if "Success" in db_response:
        res = Response(body=db_response).ok()
    else:
        res = Response(body=db_response).error()

    assert res == {
        "statusCode": 400,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"Error": "Something went wrong.", "Message": "One or more parameter values were invalid: Missing the key genre in the item"}',  # noqa
    }


# CREATE AND UPDATE MISSING BODY
def test_lambda_handler_create_and_update_error_missing_body(
    dynamodb_client, dynamodb_create_table, event_missing_body, context=None
):

    data = event_body_to_dict(event_missing_body)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.create_and_update(data=data)

    if "Success" in db_response:
        res = Response(body=db_response).ok()
    else:
        res = Response(body=db_response).error()

    assert res == {
        "statusCode": 400,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": (
            '{"Error": "Something went wrong.", "Message": '
            '"One or more parameter values were invalid: Missing the key movieName in the item"}'
        ),
    }


# CREATE AND UPDATE UPDATE OK
def test_lambda_handler_update_dynamodb(
    dynamodb_client, dynamodb_create_table, event_dynamodb_update, context=None
):
    data = event_body_to_dict(event_dynamodb_update)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.update(
        table_primary_key="movieName",
        value_primary_key=data["movieName"],
        update_expression="SET rate=:rate",
        expression_values={":rate": data["rate"]},
    )

    if "Success" in db_response:
        res = Response(body=db_response).ok()
    else:
        res = Response(body=db_response).error()

    assert res == {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": ('{"Success": "Updated fields."}'),
    }


# CREATE AND UPDATE UPDATE ERROR
def test_lambda_handler_update_dynamodb_invalid_expression(
    dynamodb_client, dynamodb_create_table, event_dynamodb_update, context=None
):
    data = event_body_to_dict(event_dynamodb_update)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.update(
        table_primary_key="movieName",
        value_primary_key=data["movieName"],
        update_expression="set rate=:rate",
        expression_values={":rte": data["rate"]},
    )

    if "Success" in db_response:
        res = Response(body=db_response).ok()
    else:
        res = Response(body=db_response).error()

    assert res == {
        "statusCode": 400,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": (
            '{"Error": "Something went wrong.", "Message": "Invalid UpdateExpression: An expression attribute value used in expression is not defined; attribute value: :rate"}'  # noqa
        ),
    }


# READ OK
def test_lambda_handler_read_ok_dynamodb(
    dynamodb_client, dynamodb_put_item, event_read, context=None
):

    data = event_body_to_dict(event_read)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.read(
        table_primary_key="movieName", value_primary_key=data["movieName"]
    )

    assert db_response == {
        "movieName": "The Dark Knight",
        "year": "2008",
        "genre": "action",
    }


# READ WITH RANGE OK
def test_lambda_handler_read_with_range_ok_dynamodb(
    dynamodb_client, dynamodb_put_item_with_range, event_read, context=None
):
    data = event_body_to_dict(event_read)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.read(
        table_primary_key="movieName",
        value_primary_key=data["movieName"],
        table_sort_key="genre",
        value_sort_key=data["genre"],
    )

    assert db_response == {
        "movieName": "The Dark Knight",
        "year": "2008",
        "genre": "action",
    }


# READ ERROR
def test_lambda_handler_read_invalid_dynamodb(
    dynamodb_client, dynamodb_put_item, event_read_invalid, context=None
):
    data = event_body_to_dict(event_read_invalid)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.read(
        table_primary_key="movieName", value_primary_key=data["movieName"]
    )

    assert (
        db_response
        == "No items found. Check your request - query: {'movieName': 'The Dark'}"
    )


# READ WITH RANGE ERROR
def test_lambda_handler_read_with_range_invalid_dynamodb(
    dynamodb_client, dynamodb_put_item_with_range, event_read_invalid, context=None
):
    data = event_body_to_dict(event_read_invalid)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.read(
        table_primary_key="movieName", value_primary_key=data["movieName"]
    )

    assert db_response == {
        "Error": "Something went wrong.",
        "Message": "Validation Exception",
    }


# DELETE
def test_lambda_handler_delete(
    dynamodb_client, dynamodb_put_item, event_read, context=None
):
    data = event_body_to_dict(event_read)

    ddbclient = DynamoDBClient(table_name="movies-prd")
    db_response = ddbclient.delete(
        table_primary_key="movieName",
        value_primary_key=data["movieName"],
    )

    print(db_response)

    assert db_response == {"Success": "Deleted item from database."}
