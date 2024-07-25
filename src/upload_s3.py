import boto3
from botocore.exceptions import NoCredentialsError, ClientError


def upload_to_s3(file_name: str, bucket: str, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Creating an S3 client
    s3_client = boto3.client("s3")

    # Check if the object already exists in the bucket
    try:
        s3_client.head_object(Bucket=bucket, Key=object_name)
        print(
            f"Error: The file '{object_name}' already exists in the bucket '{bucket}'.\n"
        )
        object_name = (
            input(
                "Enter the new name of the file OR type 'cancel' to cancel the upload: "
            )
            + ".csv"
        )
        upload_to_s3(file_name, bucket, object_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            # The object does not exist, can proceed with the upload
            pass
        else:
            # Something else has gone wrong
            print(f"Error checking if object exists: {e}")
            return False

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    return True
