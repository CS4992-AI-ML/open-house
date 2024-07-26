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
                body["body"]["Street_Display"],
                body["body"]["Street_Name"],
                body["body"]["Locality"],
                body["body"]["Postcode"],
                body["body"]["Status"],
                body["body"]["Listed_Price"],
                body["body"]["Month_Listed"],
                body["body"]["Days_Listed"],
                body["body"]["Bedrooms"],
                body["body"]["Bathrooms"],
                body["body"]["Parking"],
                body["body"]["Property_Type"],
                body["body"]["Agency_Name"],
                body["body"]["Agent"],
                body["body"]["Area"],
                body["body"]["Building_Area"],
                body["body"]["Current_Owners"],
                body["body"]["Current_Owners_Address"],
                body["body"]["PDS_Property_ID"],
                body["body"]["PDS_Listing_ID"],
                body["body"]["Government_Number"],
                body["body"]["Parent_Government_Number"],
                body["body"]["Relative_Month"],
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
    output = output["predictions"][0]["score"]
    print("Predicted Price: ", output)
    return output
