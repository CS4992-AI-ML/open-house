import boto3
import pandas as pd
from io import StringIO
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bucket_name = "team-houses-bucket"
csv_file_key = "maggie-3.csv"


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


def get_manifest_json():
    csv_data = get_csv_from_s3(bucket_name, csv_file_key)

    if csv_data is None or csv_data.empty:
        raise ValueError("DataFrame is empty or could not be retrieved.")
    else:
        logger.info(f"CSV Data from S3 Bucket: {bucket_name}")

        unique_localities = sorted(csv_data["Locality"].astype(str).unique().tolist())
        unique_agency_names = sorted(
            csv_data["Agency_Name"].astype(str).unique().tolist()
        )
        unique_agents = sorted(csv_data["Agent"].astype(str).unique().tolist())

        return {
            "localities": unique_localities,
            "agencies": unique_agency_names,
            "agents": unique_agents,
        }
