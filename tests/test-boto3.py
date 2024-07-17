import boto3

# Initialize a session using AWS credentials

# Create an S3 client
s3 = boto3.client("s3")

# List all S3 buckets
response = s3.list_buckets()

# Print bucket names
print("Existing buckets:")
for bucket in response["Buckets"]:
    print(f'  {bucket["Name"]}')
