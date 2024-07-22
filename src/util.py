import numpy as np
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import re
from datetime import datetime

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
