import os

from chalice import Chalice, Response
import boto3
import json

app = Chalice(app_name='dm-housing')
# Initialize the SageMaker runtime client
sagemaker_runtime = boto3.client('sagemaker-runtime')
# Replace with your SageMaker endpoint name
SAGEMAKER_ENDPOINT_NAME = 'dm-housing-endpoint'

@app.route('/')
def index():
    return Response(
        body=open(os.path.join(os.path.dirname(__file__), 'chalicelib/static/index.html')).read(),
        headers={'Content-Type': 'text/html'}
    )

@app.route('/predict', methods=['POST'], content_types=['application/json'])
def predict():
    request = app.current_request
    input_data = request.json_body.get('input')
    if not input_data:
        return {'error': 'Input data is required'}
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=SAGEMAKER_ENDPOINT_NAME,
        ContentType='application/json',
        Body=json.dumps({'input': input_data})
    )
    result = json.loads(response['Body'].read().decode('utf-8'))
    return {'prediction': result}

