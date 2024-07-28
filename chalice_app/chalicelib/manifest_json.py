import boto3
import pandas as pd
from io import StringIO
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bucket_name = "team-houses-bucket"
csv_file_key = "maggie-3.csv"


def manifest_json():
    def get_csv_from_s3(bucket, key):
        try:
            s3_client = boto3.client("s3")
            response = s3_client.get_object(Bucket=bucket, Key=key)
            csv_data = response["Body"].read().decode("utf-8")
            data_frame = pd.read_csv(StringIO(csv_data))
            return data_frame
        except Exception as e:
            logger.error(f"Error retrieving CSV file from S3: {e}")
            return None

    csv_data = get_csv_from_s3(bucket_name, csv_file_key)

    if csv_data is not None and not csv_data.empty:
        print(
            f"CSV Data from S3 Bucket: {bucket_name}, File: {csv_file_key}\n{csv_data.head(20)}"
        )
        # Convert DataFrame to JSON
        return json.loads(csv_data.to_json(orient="records"))
    else:
        print("DataFrame is empty or could not be retrieved.")
        return {"message": "DataFrame is empty or could not be retrieved."}


manifest_json()
