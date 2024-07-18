import boto3
import json

bucket_name = "team-houses-bucket"
json_file_key = "squid.json"

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

json_data = get_json_from_s3(bucket_name, json_file_key)

if json_data:
    print(f"JSON Data from S3: {json_data}")
else:
    print("Failed to retrieve JSON data from S3.")
