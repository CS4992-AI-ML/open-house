# `clean_data.py` - Explanation

## Overview

The `clean_data.py` script is designed to preprocess and clean housing market data from a CSV file. The script performs several data cleaning and transformation tasks to prepare the dataset for analysis. It also provides an option to upload the cleaned data to an Amazon S3 bucket.

## Step-by-Step Explanation

### 1. Load Environment Variables

The script begins by loading environment variables from a `.env` file. This file typically contains configuration settings, such as AWS credentials, which are required for connecting to external services like Amazon S3.

### 2. Define CSV File Path

Next, the script specifies the path to the CSV file that contains the housing market data. This file path points to the location where the raw data is stored.

### 3. Read CSV Data

The script then reads the CSV file into a pandas DataFrame. This DataFrame serves as the main data structure for processing and cleaning the dataset.

### 4. Drop Rows with Missing Critical Data

To ensure data quality, the script removes rows where critical columns, such as 'Month Listed' and 'Postcode', have missing values. These columns are essential for subsequent processing, so rows with missing values in these fields are excluded.

### 5. Filter Property Types

The script filters the DataFrame to include only rows where the property type is either "House" or "Unit". This step helps to focus the analysis on relevant property types and exclude any unrelated data.

### 6. Compute Weekly Price

The script calculates a new column, 'Weekly Price', based on the 'Listed Price'. It uses a custom function to convert the listed price into a weekly price format. After calculating the weekly price, it removes any rows where the weekly price is missing.

### 7. Normalize Month Columns

To standardize the 'Month Listed' column, the script creates an additional column called 'Relative Month'. This new column represents the month in a relative format for better analysis. The script also cleans the 'Month Listed' column to include only the month part and remove any extraneous text.

### 8. Standardize Locality and Postcode

The script standardizes the 'Locality' and 'Postcode' columns. It converts the locality names to uppercase to ensure consistency and formats the postcodes by prepending "X" and ensuring they are in string format.

### 9. Clean Up Data

The script sorts the DataFrame by 'Weekly Price' in ascending order, so that lower-priced listings appear first. It also updates the column names to replace spaces with underscores and removes any extra spaces for consistency.

### 10. Export Cleaned Data

The script prompts the user to enter a filename for the cleaned data. It then exports the DataFrame to a new CSV file with the specified filename in a designated directory.

### 11. Optional Upload to S3

Finally, the script asks the user whether they want to upload the cleaned CSV file to an Amazon S3 bucket. If the user agrees, it uses a custom function to upload the file to the specified S3 bucket and provides feedback on whether the upload was successful or failed. If the user declines, it notifies them that the upload was canceled.