import logging
import boto3
from botocore.exceptions import ClientError
import os
import requests


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_file_url(bucket, object_name):
    location = "us-east-2"
    url = f"https://s3-{location}.amazonaws.com/{bucket}/{object_name}"
    return url

def save_file(url, image_name):
    response = requests.get(url)
    with open(image_name, 'wb') as file:
        file.write(response.content)
    return image_name

def delete_file(image_name):
    os.remove(image_name)