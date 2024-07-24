import json
import boto3
import pandas as pd


def predict(body):
    """
    Predict backend endpoint for returning the result from our 9th model.
    :param body: Object that contains listing you want to predict
    :return: Prediction price of the listing given
    """
    sagemaker_runtime = boto3.client("sagemaker-runtime", region_name="ap-southeast-2")
    endpoint = "canvas-housing-deployment-number-1"
    df = pd.DataFrame(
        [
            [
                body["Street_Display"],
                body["Street_Name"],
                body["Locality"],
                body["Postcode"],
                body["Status"],
                body["Listed_Price"],
                body["Month_Listed"],
                body["Days_Listed"],
                body["Bedrooms"],
                body["Bathrooms"],
                body["Parking"],
                body["Property Type"],
                body["Agency Name"],
                body["Agent"],
                body["Area"],
                body["Building_Area"],
                body["Current_Owners"],
                body["Current_Owners_Address"],
                body["PDS_Property_ID"],
                body["PDS_Listing_ID"],
                body["Government_Number"],
                body["Parent_Government_Number"],
                body["Relative_Month"],
            ]
        ]
    )

    body = df.to_csv(header=False, index=False).encode("utf-8")

    print("Body content:")
    print(body.decode("utf-8"))

    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint,
        ContentType="text/csv",
        Body=body,
        Accept="application/json",
    )
    output = json.loads(response["Body"].read().decode("utf-8"))
    print(output)
    return output
