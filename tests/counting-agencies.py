import random
import time
import boto3
import pandas as pd
from botocore.exceptions import NoCredentialsError, ValidationError
import matplotlib.pyplot as plt

lessThanAgencies = {}
greaterThanAgencies = {}

# Initialize a session using Amazon S3
s3 = boto3.client("s3")

# Specify the bucket name and the name you want to give the file
bucket_name = "team-houses-bucket"
key = "maggie-3.csv"
name = "housing-data"
nameCSV = "../data/housing-data.csv"

# Download the file from S3
s3.download_file(bucket_name, key, nameCSV)

print(f"File {key} downloaded from bucket {bucket_name} to {nameCSV}\n")

# Read the downloaded CSV file into a DataFrame
df = pd.read_csv(nameCSV)

# Replace the contents of the specified columns with blank space
df["Agency_Name"] = ""
df["Agent"] = ""
df.drop(columns=["Weekly_Price"], inplace=True)

# Save the modified DataFrame to a new CSV file
df.to_csv("../data/" + name + "-noAgencies.csv", index=False)

print(f"Modified file saved to {name}-noAgencies.csv")


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


file_name = "housing-data-noAgencies.csv"
bucket_name = "team-houses-bucket"
object_name = file_name
if object_name.casefold() != "cancel.csv".casefold():
    success = upload_to_s3(file_name, bucket_name, object_name)
    if success:
        print("Upload Successful")
    else:
        print("Upload Failed")
else:
    print("Upload Cancelled")

sagemaker_client = boto3.client("sagemaker")

# Define your input and output locations in S3
input_s3_uri = f"s3://{bucket_name}/{file_name}"
output_s3_uri = f"s3://{bucket_name}/{file_name}-output"

num_columns = len(df.columns)
print(f"Number of columns: {num_columns}")

# Define your model details
model_name = "canvas-model-2024-07-25-00-01-31-123032"

# List models
response = sagemaker_client.list_models()
models = response["Models"]
for model in models:
    print(model["ModelName"])

# Open the file and read lines
with open("../data/lessThanAgencies.txt") as f:
    for line in f:
        # Strip newline characters
        stripped_line = line.strip()
        if stripped_line != "":
            # If the line is already in the dictionary, increment its count
            if stripped_line in lessThanAgencies:
                lessThanAgencies[stripped_line] += 1
            # If the line is not in the dictionary, add it with a count of 1
            else:
                lessThanAgencies[stripped_line] = 1

with open("../data/greaterThanAgencies.txt") as f:
    for line in f:
        # Strip newline characters
        stripped_line = line.strip()
        if stripped_line != "":
            # If the line is already in the dictionary, increment its count
            if stripped_line in greaterThanAgencies:
                greaterThanAgencies[stripped_line] += 1
            # If the line is not in the dictionary, add it with a count of 1
            else:
                greaterThanAgencies[stripped_line] = 1

sorted_lessThanAgencies = sorted(
    lessThanAgencies.items(), key=lambda item: item[1], reverse=True
)
sorted_greaterThanAgencies = sorted(
    greaterThanAgencies.items(), key=lambda item: item[1], reverse=True
)

# Create the absolute_agencies dictionary
absolute_agencies = {}
all_agencies = set(lessThanAgencies.keys()).union(greaterThanAgencies.keys())

for agency in all_agencies:
    less_count = lessThanAgencies.get(agency, 0)
    greater_count = greaterThanAgencies.get(agency, 0)
    absolute_agencies[agency] = less_count - greater_count

sorted_absoluteAgenciesDescending = sorted(
    absolute_agencies.items(), key=lambda item: item[1], reverse=True
)
sorted_absoluteAgenciesAscending = sorted(
    absolute_agencies.items(), key=lambda item: item[1], reverse=False
)

print(sorted_lessThanAgencies)
print("Length: " + str(len(lessThanAgencies)))
print(sorted_greaterThanAgencies)
print("Length: " + str(len(greaterThanAgencies)))

# Print the absolute_agencies dictionary
print("These agencies typically value properties lower than the predicted price:")
print(sorted_absoluteAgenciesDescending)
print("These agencies typically value properties higher than the predicted price:")
print(sorted_absoluteAgenciesAscending)

# x-coordinates of left sides of bars
left = []
# heights of bars
height = []
# labels for bars
tick_label = []

for i in range(0, 5):
    left.append(i)
    height.append(sorted_absoluteAgenciesAscending[i][1])
    tick_label.append(sorted_absoluteAgenciesAscending[i][0].replace(" ", "\n"))

# plotting a bar chart
plt.bar(left, height, tick_label=tick_label, width=0.8, color=["blue"])

# naming the x-axis
plt.xlabel("Agency")
# naming the y-axis
plt.ylabel("Score")
# plot title
plt.title("Agencies that price under predicted")
# function to show the plot
plt.show()

# x-coordinates of left sides of bars
left = []
# heights of bars
height = []
# labels for bars
tick_label = []

for i in range(0, 5):
    left.append(i)
    height.append(sorted_absoluteAgenciesDescending[i][1])
    tick_label.append(sorted_absoluteAgenciesDescending[i][0].replace(" ", "\n"))

# plotting a bar chart
plt.bar(left, height, tick_label=tick_label, width=0.8, color=["blue"])

# naming the x-axis
plt.xlabel("Agency")
# naming the y-axis
plt.ylabel("Score")
# plot title
plt.title("Agencies that price over predicted")
# function to show the plot
plt.show()
