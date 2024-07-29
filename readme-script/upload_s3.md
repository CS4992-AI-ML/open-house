# `upload_s3.py` - Explanation

## Overview

The `upload_s3.py` script provides a function to upload a file from your local system to an Amazon S3 bucket. It handles potential issues such as file existence in the bucket and missing AWS credentials.

## Step-by-Step Explanation

### 1. Import Required Libraries

The script starts by importing necessary libraries:
- **`boto3`**: The AWS SDK for Python, which is used to interact with the Amazon S3 service.
- **`NoCredentialsError`** and **`ClientError`** from **`botocore.exceptions`**: These are used for handling exceptions related to AWS credentials and general client errors.

### 2. Define `upload_to_s3` Function

The `upload_to_s3` function is responsible for uploading a file to an S3 bucket and includes error handling for various scenarios.

- **Function Steps**:
  
  1. **Determine the Object Name**:
     - **Purpose**: Decide on the name of the file as it will appear in S3.
     - **Action**: If `object_name` is not provided, it defaults to the value of `file_name`. This means the file will be uploaded with its original name.
  
  2. **Create an S3 Client**:
     - **Purpose**: Establish a connection to the S3 service.
     - **Action**: Create an S3 client using the `boto3` library. This client will be used to perform S3 operations.
  
  3. **Check if the File Already Exists in S3**:
     - **Purpose**: Ensure that the file does not overwrite an existing file unless intended.
     - **Action**: Use the `head_object` method to check if a file with the specified `object_name` already exists in the bucket.
       - **File Exists**: If the file exists, print an error message and prompt the user to provide a new name or cancel the upload.
       - **File Does Not Exist**: If the file does not exist, proceed with the upload.
  
  4. **Handle Errors in File Existence Check**:
     - **Purpose**: Manage potential issues encountered during the file existence check.
     - **Action**: Handle different scenarios:
       - **File Exists**: Prompt the user for a new file name and call the function recursively.
       - **Other Errors**: Print an error message and terminate the function if there are issues other than "file not found" (e.g., permission issues).
  
  5. **Upload the File**:
     - **Purpose**: Transfer the file from the local system to the S3 bucket.
     - **Action**: Attempt to upload the file using the `upload_file` method of the S3 client.
       - **File Not Found**: Print an error message and return `False` if the file is not found on the local system.
       - **No Credentials**: Print an error message and return `False` if AWS credentials are missing.
  
  6. **Return Upload Status**:
     - **Purpose**: Indicate the success or failure of the file upload.
     - **Action**: Return `True` if the file is successfully uploaded. Return `False` if any issues occurred during the upload process.