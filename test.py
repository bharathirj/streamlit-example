# create a S3 file upload program
import boto3
import os
from botocore.exceptions import ClientError, NoCredentialsError
import logging

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an Amazon S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    
    # Input validation
    if not file_name or not bucket:
        logging.error("File name and bucket name are required")
        return False
    
    # Check if file exists
    if not os.path.isfile(file_name):
        logging.error(f"File {file_name} does not exist")
        return False
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(file_name, bucket, object_name)
        logging.info(f"File {file_name} uploaded to {bucket}/{object_name}")
        return True
    except FileNotFoundError:
        logging.error(f"The file {file_name} was not found")
        return False
    except NoCredentialsError:
        logging.error("Credentials not available")
        return False
    except ClientError as e:
        logging.error(f"Error uploading file: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False

