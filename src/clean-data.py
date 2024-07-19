import pandas as pd
import numpy as np
from dotenv import load_dotenv
import re
from datetime import datetime

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

# Compute the average number of bathrooms per bedroom, ignoring rows where bedrooms or bathrooms are zero
bathrooms_per_bedroom = (
    df.loc[(df["Bedrooms"] != 0) & (df["Bathrooms"] != 0), "Bathrooms"]
    / df.loc[(df["Bedrooms"] != 0) & (df["Bathrooms"] != 0), "Bedrooms"]
)
avg_bathrooms_per_bedroom = bathrooms_per_bedroom.mean()

# Update the "Bathrooms" column where it is 0 and "Bedrooms" is not
df.loc[(df["Bathrooms"] == 0) & (df["Bedrooms"] != 0), "Bathrooms"] = np.round(
    df["Bedrooms"] * avg_bathrooms_per_bedroom
)

# Compute the average number of bedrooms per bathroom, ignoring rows where bedrooms or bathrooms are zero
bedrooms_per_bathroom = (
    df.loc[(df["Bedrooms"] != 0) & (df["Bathrooms"] != 0), "Bedrooms"]
    / df.loc[(df["Bedrooms"] != 0) & (df["Bathrooms"] != 0), "Bathrooms"]
)
avg_bedrooms_per_bathroom = bedrooms_per_bathroom.mean()

# Update the "Bedrooms" column where it is 0 and "Bathrooms" is not
df.loc[(df["Bedrooms"] == 0) & (df["Bathrooms"] != 0), "Bedrooms"] = np.round(
    df["Bathrooms"] * avg_bedrooms_per_bathroom
)


print("Average bathrooms per bedroom:", avg_bathrooms_per_bedroom)
print("Average bedrooms per bathroom:", avg_bedrooms_per_bathroom)

df = df.dropna(subset=["Month Listed", "Postcode"])

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
