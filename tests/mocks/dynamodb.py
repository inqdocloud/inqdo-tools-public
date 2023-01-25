import boto3
import pytest
from moto import mock_dynamodb


@pytest.fixture()
def dynamodb_client(aws_credentials):
    with mock_dynamodb():
        conn = boto3.resource("dynamodb", region_name="eu-west-1")
        yield conn


@pytest.fixture()
def event_create_and_update():
    event = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"movieName": "The Dark Knight", "year": "2008", "genre": "action"}',
    }
    return event


@pytest.fixture()
def event_create_and_update_range():
    event = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"movieName": "The Dark Knight", "year": "2008", "genre": "action"}',
    }
    return event


@pytest.fixture()
def event_create_and_update_range_missing_keys():
    event = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"movieName": "The Dark Knight", "year": "2008"}',
    }
    return event


@pytest.fixture()
def event_missing_primary_key():
    event = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"year": "2008", "genre": "action"}',
    }
    return event


@pytest.fixture()
def event_missing_body():
    event = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        }
    }
    return event


@pytest.fixture
def event_dynamodb_update(dynamodb_client):
    event = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"movieName": "The Dark Knight", "year": "2008", "genre": "action", "rate": "8.3"}',
    }
    return event


@pytest.fixture
def event_read(dynamodb_client):
    event = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"movieName": "The Dark Knight", "genre": "action"}',
    }
    return event


@pytest.fixture
def event_read_invalid(dynamodb_client):
    event = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"movieName": "The Dark", "genre": "action"}',
    }
    return event


@pytest.fixture
def event_read_with_range_key_missing_invalid(dynamodb_client):
    event = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"movieName": "The Dark Knight",}',
    }
    return event


@pytest.fixture
def dynamodb_create_table(dynamodb_client):
    dynamodb_client.create_table(
        TableName="movies-prd",
        KeySchema=[
            {"AttributeName": "movieName", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "movieName", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    yield


@pytest.fixture
def dynamodb_create_table_query(dynamodb_client):
    dynamodb_client.create_table(
        TableName="players-prd",
        KeySchema=[
            {"AttributeName": "name", "KeyType": "HASH"},
            {"AttributeName": "number", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "name", "AttributeType": "S"},
            {"AttributeName": "number", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    yield


@pytest.fixture
def dynamodb_create_table_with_range_key(dynamodb_client):
    dynamodb_client.create_table(
        TableName="movies-prd",
        KeySchema=[
            {"AttributeName": "movieName", "KeyType": "HASH"},
            {"AttributeName": "genre", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "movieName", "AttributeType": "S"},
            {"AttributeName": "genre", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    yield


@pytest.fixture
def dynamodb_put_item(dynamodb_create_table, dynamodb_client):
    table_connection = dynamodb_client.Table("movies-prd")
    table_connection.put_item(
        Item={"movieName": "The Dark Knight", "year": "2008", "genre": "action"}
    )
    yield


@pytest.fixture
def dynamodb_put_item_for_query(dynamodb_create_table_query, dynamodb_client):
    table_connection = dynamodb_client.Table("players-prd")
    table_connection.put_item(Item={"name": "inQdo", "number": "5"})
    yield


@pytest.fixture
def dynamodb_put_item_with_range(dynamodb_create_table_with_range_key, dynamodb_client):
    table_connection = dynamodb_client.Table("movies-prd")
    table_connection.put_item(
        Item={"movieName": "The Dark Knight", "year": "2008", "genre": "action"}
    )
    yield
