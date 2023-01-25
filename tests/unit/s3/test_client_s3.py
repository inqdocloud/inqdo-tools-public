from io import BytesIO

from inqdo_tools.s3.client import S3Client


# LIST OBJECT
def test_list_object(s3_client, s3_create_bucket, s3_put_object_txt):
    s3_client = S3Client(bucket_name="s3-test")

    response = s3_client.list_objects()

    found_object = [
        s3_object["Key"]
        for s3_object in response
        if s3_object["Key"] == "test-file.txt"
    ]

    assert found_object == ["test-file.txt"]


# GET OBJECT TXT
def test_get_object_txt(s3_client, s3_create_bucket, s3_put_object_txt):
    s3_client = S3Client(bucket_name="s3-test")

    response = s3_client.get_object(object_key="test-file.txt")
    assert response == "test content"


# GET OBJECT JSON
def test_get_object_json(s3_client, s3_create_bucket, s3_put_object_json):
    s3_client = S3Client(bucket_name="s3-test")

    response = s3_client.get_object(object_key="test-file.json", json_loads=True)

    assert response == {"test": "abc"}


# GET OBJECT NOT FOUND
def test_get_object_not_found(s3_client, s3_create_bucket, s3_put_object_json):
    s3_client = S3Client(bucket_name="s3-test")

    response = s3_client.get_object(object_key="test-fi.json")

    assert response == {
        "Error": "Something went wrong.",
        "Message": "The specified key does not exist.",
    }


# UPOAD FILE OBJECT
def test_upload_file_object(s3_client, s3_create_bucket):
    s3_client = S3Client(bucket_name="s3-test")
    with open("tests/unit/s3/test.xlsx", "rb") as fh:
        xlsx_data = BytesIO(fh.read())

        response = s3_client.upload_fileobj(data=xlsx_data, file_name="test.xlsx")

    assert response == "Uploaded file: test.xlsx"


# DELETE FILE OBJECT
def test_delete_object(s3_client, s3_create_bucket, s3_put_object_json):
    s3_client = S3Client(bucket_name="s3-test")
    response = s3_client.delete_object(object_key="test-file.json")

    assert response == "Successfull deleted object: test-file.json"
