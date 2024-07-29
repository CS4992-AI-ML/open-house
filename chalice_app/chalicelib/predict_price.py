import json
import boto3
import pandas as pd
import numpy as np


def predict_price(body):
    """
    Predict backend endpoint for returning the result from our 9th model.
    :param body: Object that contains listing you want to predict
    :return: Prediction price of the listing given
    """
    sagemaker_runtime = boto3.client("sagemaker-runtime", region_name="ap-southeast-2")
    endpoint = "canvas-housing-deployment-number-1"

    raw_postcode = body.get("postcode")
    df = pd.DataFrame(
        [
            [
                np.nan,
                np.nan,
                body.get("locality", np.nan),
                "X" + raw_postcode if raw_postcode is not None else np.nan,
                "Current",
                np.nan,
                body.get("monthListed", "Jun"),
                body.get("daysListed", 0),
                body.get("bedrooms", np.nan),
                body.get("bathrooms", np.nan),
                body.get("parkingSpaces", np.nan),
                body.get("propertyType", "Unit"),
                body.get("agencyName", np.nan),
                body.get("agentName", np.nan),
                body.get("landArea", np.nan),
                body.get("floorArea", np.nan),
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                body.get("relativeMonth", 0),
            ]
        ]
    )

    body = df.to_csv(header=False, index=False).encode("utf-8")

    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint,
        ContentType="text/csv",
        Body=body,
        Accept="application/json",
    )

    body = response["Body"].read()

    output = json.loads(body.decode("utf-8"))
    return output["predictions"][0]["score"]
