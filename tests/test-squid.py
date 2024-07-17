import boto3
import json
import pandas as pd
from io import StringIO

bucket_name = "team-houses-bucket"
json_file_key = "squid.json"
csv_file_key = "housing_data.csv"


# Gets JSON data from a specific bucket and key
def get_json_from_s3(bucket, key):
    try:
        s3_client = boto3.client("s3")
        response = s3_client.get_object(Bucket=bucket, Key=key)
        json_data_2 = json.loads(response["Body"].read().decode("utf-8"))
        return json_data_2
    except Exception as e:
        print(f"Error retrieving JSON file from S3: {e}")
        return None


# Gets CSV data from a specific bucket and key
def get_csv_from_s3(bucket, key):
    try:
        s3_client = boto3.client("s3")
        response = s3_client.get_object(Bucket=bucket, Key=key)
        csv_data2 = response["Body"].read().decode("utf-8")
        data_frame = pd.read_csv(StringIO(csv_data2))
        return data_frame
    except Exception as e:
        print(f"Error retrieving CSV file from S3: {e}")
        return None


def get_column_from_s3(data_frame, column_name):
    return csv_data[column_name]


json_data = get_json_from_s3(bucket_name, json_file_key)
csv_data = get_csv_from_s3(bucket_name, csv_file_key)
column_name = 'Agent'

# Prints out the first 20 lines of the csv_data file
if csv_data is not None and not csv_data.empty:
    print(
        f"CSV Data from \nS3 Bucket: [{bucket_name}] \nFile: [{csv_file_key}] \n{csv_data.head(20)}\n")
else:
    print("DataFrame is empty or could not be retrieved.")

# Prints out the first 20 lines of the given column set in column_name
print(
    f"Column data for column: \n[{column_name}] in [{csv_file_key}] "
    f"\n{get_column_from_s3(csv_data, column_name).head(20)}")

# Prints out the contents of json_data
if json_data:
    print(f"JSON Data from \nS3 Bucket: [{bucket_name}] \nFile: [{json_file_key}] \n{json_data}")
else:
    print("Failed to retrieve JSON data from S3.")
