from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

print('Text Detection Using Azure Cognitive services, Computer Vision API')

#Auntheticate your credentials and create a client
subscription_key = "put_your_key_here"
endpoint = "put_endpoint_location_here"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

print('=== Read file ===')

read_image_path = './images/handwritten_text.jpg'

read_image = open(read_image_path, 'rb')

read_response = computervision_client.read_in_stream(read_image, raw = True)

read_operation_location = read_response.headers['Operation-Location']

operation_id = read_operation_location.split('/')[-1]

print('Generating detection below......')

# Call the 'GET' API and wait for the retrieval of results
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                

# Print results, line by line
if read_results.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)


print()
print('Detection is complete')

