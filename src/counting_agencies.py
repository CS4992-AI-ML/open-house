from io import StringIO, BytesIO

import boto3
import pandas as pd
from botocore.exceptions import NoCredentialsError
from sagemaker import TrainingInput
import matplotlib.pyplot as plt
import matplotlib

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


def upload_to_s3(new_name, bucket):
    """
    Upload a file to an S3 bucket

    :param new_name: File to upload
    :param bucket: Bucket to upload to
    :return: True if file was uploaded, else False
    """
    # Upload the file
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(new_name, bucket, object_name)
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
    success = upload_to_s3("../data/" + file_name, bucket_name)
    if success:
        print("Upload Successful")
    else:
        print("Upload Failed")
else:
    print("Upload Cancelled")

sagemaker_client = boto3.client("sagemaker")

# Define your input and output locations in S3
s3_data_path = f"s3://{bucket_name}/{file_name}"

# Create a dataset object
dataset = TrainingInput(s3_data_path, content_type="csv")

num_columns = len(df.columns)
print(f"Number of columns: {num_columns}")

# Specify the bucket name and the name you want to give the file
bucket_name = "sagemaker-ap-southeast-2-923732660828"
key = (
    "Canvas/owen/Inference/26d37167-6ca8-4646-b807-ef397e1ce856"
    "/prediction/26d37167-6ca8-4646-b807-ef397e1ce856_full_prediction.csv"
)
nameCSV = "prediction.csv"

specific_folder = "Canvas/owen/Inference/"

# List objects within the specific folder
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=specific_folder, Delimiter="/")

# Get all the folders (common prefixes) within the specific folder
folders = response.get("CommonPrefixes")

# Dictionary to store the first file in each subfolder
first_files = {}

download_path = "../data/prediction.csv"

if folders:
    for folder in folders:
        folder_prefix = folder["Prefix"]

        # List objects within the subfolder
        folder_objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)

        # Get the first file
        if "Contents" in folder_objects:
            first_file = folder_objects["Contents"][0]["Key"]

            # Download the first file
            s3.download_file(bucket_name, first_file, download_path)
            print(f"Downloaded {first_file} to {download_path}")
            break  # Stop after downloading the first file
else:
    print("No subfolders found in the specified folder.")

# List models
response = sagemaker_client.list_models()
models = response["Models"]
# for model in models:
#    print(model["ModelName"])

original = pd.read_csv("../data/housing-data.csv")
predicted = pd.read_csv("../data/prediction.csv")

weekly_price_array = original["Weekly_Price"].to_numpy()
predicted_price_array = predicted["Weekly_Price"].to_numpy()
agencies = original["Agency_Name"]
differences = []
differenceDict = {}

for i in range(0, len(weekly_price_array)):
    differences += [
        (weekly_price_array[i] - predicted_price_array[i]) / weekly_price_array[i]
    ]
    if agencies[i] in differenceDict:
        differenceDict[agencies[i]] = differenceDict[agencies[i]] + differences[i]
    else:
        differenceDict[agencies[i]] = differences[i]

sorted_absoluteAgenciesDescending = sorted(
    differenceDict.items(), key=lambda item: item[1], reverse=True
)
sorted_absoluteAgenciesAscending = sorted(
    differenceDict.items(), key=lambda item: item[1], reverse=False
)

# Print the absolute_agencies dictionary
print("These agencies typically value properties lower than the predicted price:")
print(sorted_absoluteAgenciesDescending[:5])
print("These agencies typically value properties higher than the predicted price:")
print(sorted_absoluteAgenciesAscending[:5])
bucket_name = "team-houses-bucket"


def generate_graph(data, colors, title):
    # x-coordinates of left sides of bars
    left = []
    # heights of bars
    height = []
    # labels for bars
    tick_label = []

    for item in range(0, 10):
        left.append(item)
        height.append(data[item][1])
        tick_label.append(data[item][0].replace(" ", "\n"))

    colormap = matplotlib.colormaps[colors]  # You can choose any colormap here
    start, end = 0.6, 1.1  # Adjust these values to shift the brightness
    colors = [
        colormap(start + (end - start) * i / (len(left) - 1)) for i in range(len(left))
    ]

    plt.figure(figsize=(8, 6))
    # plotting a bar chart
    plt.bar(
        left,
        height,
        tick_label=tick_label,
        width=0.8,
        color=colors,
    )

    # Change the fontsize to the desired value
    plt.xticks(fontsize=6)
    # naming the x-axis
    plt.xlabel("Agency")
    # naming the y-axis
    plt.ylabel("Score")
    # plot title
    plt.title(title)
    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(
        img_buffer, format="png", bbox_inches="tight", dpi=300
    )  # Save as PNG image
    img_buffer.seek(0)  # Rewind the buffer to the beginning
    plt.close()  # Close the plot to free up memory

    s3_file_path = (title + ".png").replace(" ", "_")

    # Upload the PNG image to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=s3_file_path,
        Body=img_buffer.getvalue(),
        ContentType="image/png",
    )

    print(f"Bar chart successfully uploaded to s3://{bucket_name}/{s3_file_path}")


generate_graph(sorted_absoluteAgenciesAscending, "Blues", "Underpricing_Agencies")
generate_graph(sorted_absoluteAgenciesDescending, "Reds", "Overpricing_Agencies")

sorted_data = dict(
    sorted(differenceDict.items(), key=lambda item: item[1]), reverse=True
)

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(
    list(sorted_data.items()),
    columns=["Agency Name", "Score [Lower values signify overpricing]"],
)

# Create a CSV buffer
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

# Initialize the S3 client
s3 = boto3.client("s3")

# Specify the desired path in your S3 bucket
s3_file_path = "scoreOutput.csv"

# Upload the CSV to S3
s3.put_object(Bucket=bucket_name, Key=s3_file_path, Body=csv_buffer.getvalue())

print(f"CSV file successfully uploaded to s3://{bucket_name}/{s3_file_path}")
