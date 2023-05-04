from dynamodb.client import DynamoDBClient, ComparisonOperators


# CREATE AND UPDATE
def test_create_and_update(dynamodb_resource, dynamodb_create_table):

    ddbclient = DynamoDBClient(table_name="movies-prd")

    response = ddbclient.create_and_update(
        data={"movieName": "The Dark Knight", "year": "2008", "genre": "action"}
    )

    assert response == {"Success": "Saved or updated item."}


# CREATE AND UPDATE MISSING PRIMARY KEY
def test_create_and_update_missing_primary_key(dynamodb_resource, dynamodb_create_table):

    ddbclient = DynamoDBClient(table_name="movies-prd")

    response = ddbclient.create_and_update(data={"year": "2008", "genre": "action"})

    assert response == {
        "Error": "Something went wrong.",
        "Message": "One or more parameter values were invalid: Missing the key movieName in the item",
    }


# CREATE AND UPDATE BATCH
def test_create_and_update_batch(dynamodb_resource, dynamodb_create_table):

    ddbclient = DynamoDBClient(table_name="movies-prd")

    data = ddbclient.create_and_update_batch(
        batch_list=[
            {"movieName": "The Dark Knight", "year": "2008", "genre": "1972"},
            {"movieName": "The Godfather", "year": "2008", "genre": "crime"},
        ]
    )

    assert data == {"Success": "Saved or updated items in batch."}


# CREATE AND UPDATE BATCH MISSING PRIMARY KEY
def test_create_and_update_batch_missing_primary_key(
    dynamodb_resource, dynamodb_create_table
):

    ddbclient = DynamoDBClient(table_name="movies-prd")

    data = ddbclient.create_and_update_batch(
        batch_list=[
            {"year": "2008", "genre": "1972"},
            {"movieName": "The Godfather", "year": "2008", "genre": "crime"},
        ]
    )

    assert data != {"Success": "Saved or updated items in batch."}


# DELETE
def test_delete(dynamodb_resource, dynamodb_create_table, dynamodb_put_item):

    ddbclient = DynamoDBClient(table_name="movies-prd")

    data = ddbclient.delete(
        table_primary_key="movieName", value_primary_key="The Dark Knight"
    )

    assert data == {"Success": "Deleted item from database."}


# DELET BATCH
def test_delete_batch(dynamodb_resource, dynamodb_create_table):

    ddbclient = DynamoDBClient(table_name="movies-prd")

    data = ddbclient.delete_batch(
        table_primary_key="movieName", batch_list=["The Dark Knight", "The Godfather"]
    )

    assert data == {"Success": "Deleted items in batch."}


# READ
def test_read(dynamodb_resource, dynamodb_create_table, dynamodb_put_item):

    ddbclient = DynamoDBClient(table_name="movies-prd")

    data = ddbclient.read(
        table_primary_key="movieName", value_primary_key="The Dark Knight"
    )

    assert data == {"movieName": "The Dark Knight", "year": "2008", "genre": "action"}


# READ SORT KEY
def test_read_with_sort_key(
    dynamodb_resource, dynamodb_create_table_with_range_key, dynamodb_put_item_with_range
):

    ddbclient = DynamoDBClient(table_name="movies-prd")

    data = ddbclient.read(
        table_primary_key="movieName",
        value_primary_key="The Dark Knight",
        table_sort_key="genre",
        value_sort_key="action",
    )

    assert data == {"movieName": "The Dark Knight", "year": "2008", "genre": "action"}


# READ ALL
def test_read_all(dynamodb_resource, dynamodb_create_table, dynamodb_put_item):

    ddbclient = DynamoDBClient(table_name="movies-prd")

    data = ddbclient.read_all()

    assert data == [{"movieName": "The Dark Knight", "year": "2008", "genre": "action"}]


# QUERY
def test_query_single(
    dynamodb_resource, dynamodb_create_table, dynamodb_put_item_for_query
):

    ddbclient = DynamoDBClient(table_name="players-prd")

    data = ddbclient.query(
        table_primary_key="name",
        query_value="inQdo",
    )

    assert data == [{"name": "inQdo", "number": "5"}]


# QUERY WITH SORT KEY
def test_query_with_sort_key(
    dynamodb_resource, dynamodb_create_table, dynamodb_put_item_for_query
):

    ddbclient = DynamoDBClient(table_name="players-prd")

    data = ddbclient.query(
        table_primary_key="name",
        value_primary_key="inQdo",
        query_value="6",
        table_sort_key="number",
        comparison_operator=ComparisonOperators.LT,
    )

    assert data == [{"name": "inQdo", "number": "5"}]


# QUERY WITH SORT KEY
def test_query_no_result(
    dynamodb_resource, dynamodb_create_table, dynamodb_put_item_for_query
):

    ddbclient = DynamoDBClient(table_name="players-prd")

    data = ddbclient.query(
        table_primary_key="name",
        value_primary_key="inQdo",
        query_value="6",
        table_sort_key="number",
        comparison_operator=ComparisonOperators.GE,
    )

    assert data == []


# QUERY WITH MISSING KEYS
def test_query_missing_keys(
    dynamodb_resource, dynamodb_create_table, dynamodb_put_item_for_query
):

    ddbclient = DynamoDBClient(table_name="players-prd")

    data = ddbclient.query(
        table_primary_key="name",
        value_primary_key="inQdo",
        query_value="1",
        table_sort_key="number",
    )

    assert data["Error"] == "Something went wrong."


# QUERY CLIENT
def test_client_query_single(
    dynamodb_client, dynamodb_client_create_table, dynamodb_client_put_item_for_query
):
    ddbclient = DynamoDBClient(
        table_name="players-prd",
        arn="arn:aws:iam::123456789012:role/service-role/test-role"
    )

    data = ddbclient.query(
        table_primary_key="name",
        query_value="inQdo",
    )

    assert data == [{"name": "inQdo", "number": "5"}]


# QUERY CLIENT WITH SORT KEY
def test_client_query_with_sort_key(
    dynamodb_resource, dynamodb_client_create_table, dynamodb_client_put_item_for_query
):
    ddbclient = DynamoDBClient(
        table_name="players-prd",
        arn="arn:aws:iam::123456789012:role/service-role/test-role"
    )

    data = ddbclient.query(
        table_primary_key="name",
        value_primary_key="inQdo",
        query_value="6",
        table_sort_key="number",
        comparison_operator=ComparisonOperators.LT,
    )

    assert data == [{"name": "inQdo", "number": "5"}]


# QUERY CLIENT WITH SORT KEY
def test_client_query_no_result(
    dynamodb_resource, dynamodb_client_create_table, dynamodb_client_put_item_for_query
):
    ddbclient = DynamoDBClient(
        table_name="players-prd",
        arn="arn:aws:iam::123456789012:role/service-role/test-role"
    )

    data = ddbclient.query(
        table_primary_key="name",
        value_primary_key="inQdo",
        query_value="6",
        table_sort_key="number",
        comparison_operator=ComparisonOperators.GE,
    )

    assert data == []


# QUERY CLIENT WITH MISSING KEYS
def test_client_query_missing_keys(
    dynamodb_resource, dynamodb_client_create_table, dynamodb_client_put_item_for_query
):
    ddbclient = DynamoDBClient(
        table_name="players-prd",
        arn="arn:aws:iam::123456789012:role/service-role/test-role"
    )

    data = ddbclient.query(
        table_primary_key="name",
        value_primary_key="inQdo",
        query_value="1",
        table_sort_key="number",
    )

    assert data["Error"] == "Something went wrong."


# PUT ITEM
def test_put_item(dynamodb_client, dynamodb_client_create_table):
    ddbclient = DynamoDBClient(
        table_name="movies-prd",
        arn="arn:aws:iam::123456789012:role/service-role/test-role"
    )

    item = {
        "movieName": "The Dark Knight",
        "year": "2008",
        "genre": "action"
    }

    response = ddbclient.put_item(
        item=item
    )

    assert response == 200


# GET ITEM
def test_get_item(dynamodb_client, dynamodb_client_create_table, dynamodb_client_put_item):
    ddbclient = DynamoDBClient(
        table_name="movies-prd",
        arn="arn:aws:iam::123456789012:role/service-role/test-role"
    )

    data = ddbclient.get_item(
        key={"movieName": "The Dark Knight"}
    )

    assert data == {"movieName": "The Dark Knight", "year": "2008", "genre": "action"}


# UPDATE ITEM
def test_update_item(dynamodb_client, dynamodb_client_create_table, dynamodb_client_put_item):
    ddbclient = DynamoDBClient(
        table_name="movies-prd",
        arn="arn:aws:iam::123456789012:role/service-role/test-role"
    )

    Key = {"movieName": "The Dark Knight"}
    expression_attribute_names = {'#KEY': 'genre'}
    expression_attribute_values = {
        ':value': {
            'S': 'romantic',
        },
    }
    update_expression = 'SET #KEY = :value'
    data = ddbclient.update_item(
        key=Key,
        expression_attribute_names=expression_attribute_names,
        expression_attribute_values=expression_attribute_values,
        update_expression=update_expression
    )

    assert data == {"movieName": "The Dark Knight", "year": "2008", "genre": "romantic"}


# DELETE ITEM
def test_delete_item(dynamodb_client, dynamodb_client_create_table, dynamodb_client_put_item):
    ddbclient = DynamoDBClient(
        table_name="movies-prd",
        arn="arn:aws:iam::123456789012:role/service-role/test-role"
    )

    data = ddbclient.delete_item(
        key={"movieName": "The Dark Knight"}
    )

    assert data == 200
