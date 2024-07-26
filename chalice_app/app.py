import os

from chalice import Chalice, Response
import logging
import boto3
from chalicelib.predict_price import predict_price

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Chalice(app_name="dm-housing")
sagemaker_runtime = boto3.client("sagemaker-runtime")
SAGEMAKER_ENDPOINT_NAME = "dm-housing-endpoint"


@app.route("/")
def index():
    return Response(
        body=open(
            os.path.join(os.path.dirname(__file__), "chalicelib/static/index.html")
        ).read(),
        headers={"Content-Type": "text/html"},
    )


@app.route("/predict", methods=["POST"], content_types=["application/json"])
def predict():
    logger.info("Predict endpoint called")
    request = app.current_request
    input_data = request.json_body
    if not input_data:
        return Response(
            body={"error": "Input data is required"},
            status_code=404,
            headers={"Content-Type": "application/json"},
        )

    try:
        response = predict_price(input_data)
    except Exception as e:
        logger.error("Error during prediction: %s", e)
        return Response(
            body={
                "error": f"Failed to invoke the SageMaker endpoint [{type(e).__name__}]"
            },
            status_code=500,
            headers={"Content-Type": "application/json"},
        )

    logger.info("Predicted Price: %s", response)
    return {"prediction": response}
