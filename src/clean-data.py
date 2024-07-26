import boto3
import pandas as pd
from dotenv import load_dotenv
import re
from datetime import datetime
from botocore.exceptions import NoCredentialsError, ClientError

# Load the .env file
load_dotenv()

# CSV file path
csv_file_path = "../data/housing_data.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

df.drop(
    columns=[
        "Status",
        "Current Owners",
        "Current Owners Address",
        "PDS Property ID",
        "PDS Listing ID",
        "Government Number",
        "Parent Government Number",
        "Building Area",
        "Street Display",
    ],
    inplace=True,
)

# Drop rows where Property Type is not Housing or Unit
df = df[df["Property Type"].isin(["House", "Unit"])]

# Drop rows where any area value is 0
df = df[~(df[["Area"]] == 0).any(axis=1)]

# Regular expression pattern to find weekly price
pattern = r"\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?!(?:per\s*month|month|/m))\s*(?:per\s*week|week|wk|w|pw)?"


# Function to extract and convert price to integer
def extract_weekly_price(text):
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        price_str = match.group(1)  # Extract the price string
        price_str = price_str.replace(",", "")
        price = int(float(price_str))  # Convert to float and then to integer
        return price
    return None


ref_date = datetime(2024, 6, 1)


def get_relative_month(text):
    date = datetime.strptime(text, "%b %Y")
    diff_years = ref_date.year - date.year
    diff_months = ref_date.month - date.month

    return diff_years * 12 + diff_months


df["Weekly Price"] = df["Listed Price"].apply(lambda x: extract_weekly_price(str(x)))
df.drop(columns=["Listed Price"], inplace=True)

df = df.dropna(
    # subset=["Month Listed", "Postcode", "Weekly Price", "Parking", "Bedrooms"]
)
df = df[df["Weekly Price"] >= 150]

# Fix month columns
df["Relative Month"] = df["Month Listed"].apply(lambda x: get_relative_month(str(x)))
df["Month Listed"] = df["Month Listed"].apply(
    lambda x: x.split(" ")[0] if isinstance(x, str) else x
)

df["Locality"] = df["Locality"].str.upper()  # Convert locality to uppercase

df["Street Name"] = df["Street Name"].str.upper()  # Convert street_name to uppercase
df["Locality"] = df["Locality"].str.upper()  # Convert locality to uppercase
df["Postcode"] = df["Postcode"].apply(
    lambda x: "X" + str(int(x))
)  # Convert postcode to string if not already

print(len(df))

df.to_csv("../data/cleaned_housing_data-nulls-fixed.csv", index=False)


def upload_to_s3(file_name, bucket, object_name=None):
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
                input("Enter the name of the file OR type 'cancel' to cancel the upload: ")
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


file_name = "../data/NoAgencies.csv"
bucket_name = "team-houses-bucket"
object_name = (
        input("Enter the name of the file OR type 'cancel' to cancel the upload: ") + ".csv"
)
if object_name.casefold() != "cancel.csv".casefold():
    success = upload_to_s3(file_name, bucket_name, object_name)
    if success:
        print("Upload Successful")
    else:
        print("Upload Failed")
else:
    print("Upload Cancelled")
