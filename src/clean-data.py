import boto3
import pandas as pd
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError

from s3 import upload_to_s3
from util import get_relative_month, extract_weekly_price

# Load the .env file
load_dotenv()

# CSV file path
csv_file_path = "../data/housing_data.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

df = df.dropna(
    subset=[
        "Month Listed",
        "Postcode",
    ]
)

# Drop rows where Property Type is not Housing or Unit
df = df[df["Property Type"].isin(["House", "Unit"])]

# Grab the weekly price
df["Weekly Price"] = df["Listed Price"].apply(lambda x: extract_weekly_price(str(x)))
df = df.dropna(
    subset=[
        "Weekly Price",
    ]
)

# Fix month columns
df["Relative Month"] = df["Month Listed"].apply(lambda x: get_relative_month(str(x)))
df["Month Listed"] = df["Month Listed"].apply(
    lambda x: x.split(" ")[0] if isinstance(x, str) else x
)

df["Locality"] = df["Locality"].str.upper()  # Convert locality to uppercase
df["Locality"] = df["Locality"].str.upper()  # Convert locality to uppercase
df["Postcode"] = df["Postcode"].apply(
    lambda x: "X" + str(int(x))
)  # Convert postcode to string if not already

print("Total rows:", len(df))

df = df.sort_values(by="Weekly Price", ascending=True)
df.columns = [col.strip().replace(" ", "_") for col in df.columns]

# Example usage
file_name = input("Enter the name of the file: \n") + ".csv"


# Export the cleaned data to a new CSV file
df.to_csv(f"../data/{file_name}", index=False)

confirmation_str = input("Upload to s3 (y/n)?\n")

if confirmation_str.casefold() == "y".casefold():
    success = upload_to_s3(f"../data/{file_name}", "team-houses-bucket", file_name)
    if success:
        print("Upload Successful")
    else:
        print("Upload Failed")
else:
    print("Upload Cancelled")
