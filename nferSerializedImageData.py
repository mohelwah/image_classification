"""
inferSerializedImageData: a lambda function for invoking the model endpoint and returning inferences
"""
import json
import base64
import boto3

# Name of the deployed model
ENDPOINT = "imageModelEndpoint2-2-2023"
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['image_data'])

    # Instantiate a Predictor
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='application/x-image', Body=image)
    inferences = response['Body'].read().decode('utf-8')
    event["inferences"] = [float(x) for x in inferences[1:-1].split(',')]
    
    # We return the data back to the Step Function    
    return {
        'statusCode': 200,
        'body': {
            "image_data": event['image_data'],
            "s3_bucket": event['s3_bucket'],
            "s3_key": event['s3_key'],
            "inferences": event['inferences'],
        }
    }
