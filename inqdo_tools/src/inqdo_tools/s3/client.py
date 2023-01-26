"""
S3 client
=========
"""
import json
import os
import tempfile
import time

import boto3
from boto3.s3.transfer import TransferConfig

if "DEBUG_INQDO_TOOLS" in os.environ.keys():
    from utils.error import ErrorHandler
else:
    from inqdo_tools.utils.error import ErrorHandler


class S3Client(object):
    """This object will construct a s3 client.

    :param region_name: An optional :class:`region_name` argument, which will determine
        the region of the bucket.
    :type region_name: str, optional, default: eu-west-1

    :rtype: dict
    """

    def __init__(self, bucket_name: str, region_name="eu-west-1", **kwargs):
        self.s3_client = boto3.client("s3", region_name=region_name)
        self.s3_resource = boto3.resource("s3", region_name=region_name)
        self.bucket_name = bucket_name
        self.temp_file = None
        self.dict = None
        self.total = 0
        self.uploaded = 0

    @ErrorHandler.base_exception
    def list_objects(self, **kwargs) -> dict:
        """List objects

        Gives back the contents of the bucket.

        :param prefix: An optional :class:`prefix` argument, which will determine
            the prefix of the object.
        :type prefix: str, optional

        :rtype: list
        """

        if "prefix" in kwargs:
            prefix = kwargs["prefix"]
            response = self.s3_client.list_objects(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
        else:
            response = self.s3_client.list_objects(
                Bucket=self.bucket_name,
            )

        if "Contents" in response:
            return response["Contents"]

        return response

    @ErrorHandler.base_exception
    def get_object(self, object_key: str, **kwargs) -> dict:
        """Get object

        :param object_key: This is the key from the specified object to get.
        :type object_key: str

        :param json_loads: This param is optional and used to preform a json.loads
        :type json_loads: bool

        :rtype: Union[str, dict]
        """
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)

        if "Body" in response:
            if "json_loads" in kwargs:
                return json.loads(response["Body"].read().decode())
            return response["Body"].read().decode()

        return response

    @ErrorHandler.base_exception
    def download_to_file(self):
        """Download an S3 object to a file."""
        temp_file = tempfile.mktemp()

        self.s3_client.download_file(
            self.bucket_name,
            self.object_key,
            temp_file,
        )

        self.temp_file = temp_file

    def upload_tracker(self, size):
        if "inqdo-test" not in os.environ:
            time.sleep(10)
        if self.total == 0:
            return
        self.uploaded += size
        print("---")
        print("UPLOADED: {}%".format(int(self.uploaded / self.total * 100)))

    @ErrorHandler.base_exception
    def upload_fileobj(self, data, file_name: str, **kwargs):
        """Upload a file to an S3 bucket
            method accepts a readable file-like object. The file object must be opened in binary mode, not text mode.

        :param data: Data _io.BytesIO to upload
        :type data: _io.BytesIO

        :param file_name: File to upload
        :type file_name: str

        :return: str
        """
        config = TransferConfig(
            multipart_threshold=1024 * 25,
            max_concurrency=10,
            multipart_chunksize=1024 * 25,
            use_threads=True,
        )

        self.total = data.getbuffer().nbytes
        self.s3_client.upload_fileobj(
            data,
            self.bucket_name,
            file_name,
            Config=config,
            Callback=self.upload_tracker,
        )

        return f"Uploaded file: {file_name}"

    @ErrorHandler.base_exception
    def copy_file_obj(self, source_bucket_name: str, source_key: str) -> dict:
        s3_copy_resource = boto3.resource("s3")

        copy_source = {"Bucket": self.bucket_name, "Key": self.object_key}

        bucket = s3_copy_resource.Bucket(source_bucket_name)
        response = bucket.copy(copy_source, source_key)

        return response

    @ErrorHandler.base_exception
    def delete_object(self, object_key):
        """Delete object

        :param object_key: This is the key from the specified object to delete.
        :type object_key: str

        :rtype: Union[str, dict]
        """
        response = self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)

        if response["ResponseMetadata"]:
            if response["ResponseMetadata"]["HTTPStatusCode"] == 204:
                return f"Successfull deleted object: {object_key}"

        return response
