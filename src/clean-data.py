import pandas as pd
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
        # "PDS Property ID",
        "PDS Listing ID",
        "Government Number",
        "Parent Government Number",
    ],
    inplace=True,
)

# Drop rows where Property Type is not Housing or Unit
df = df[df["Property Type"].isin(["Housing", "Unit"])]

# Drop rows where any area value is 0
df = df[~(df[["Area", "Building Area"]] == 0).any(axis=1)]

# Drop rows where Street Display contains a hyphen or slash
# df = df[~df["Street Display"].fillna("").str.contains(r"[-/]", na=False)]

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
    else:
        print(text)
    return None


ref_date = datetime(2024, 6, 1)


def get_relative_month(text):
    date = datetime.strptime(text, "%b %Y")
    diff_years = ref_date.year - date.year
    diff_months = ref_date.month - date.month

    return diff_years * 12 + diff_months


df["Weekly Price"] = df["Listed Price"].apply(lambda x: extract_weekly_price(str(x)))
df.drop(columns=["Listed Price"], inplace=True)

df = df.dropna()

# Fix month columns
df["Relative Month"] = df["Month Listed"].apply(lambda x: get_relative_month(str(x)))
df["Month Listed"] = df["Month Listed"].apply(
    lambda x: x.split(" ")[0] if isinstance(x, str) else x
)

df["Locality"] = df["Locality"].str.upper()  # Convert locality to uppercase

df["Street Name"] = df["Street Name"].str.upper()  # Convert street_name to uppercase
df["Locality"] = df["Locality"].str.upper()  # Convert locality to uppercase
df["Postcode"] = df["Postcode"].astype(str)  # Convert postcode to string if not already

print(len(df))
print(df.sample(100))

df.to_csv("../data/cleaned_housing_data.csv", index=False)
