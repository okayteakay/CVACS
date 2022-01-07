from io import BytesIO
import os
from PIL import Image, ImageDraw
import requests

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

local_image = ".\images\indian_street.jpg"
remote_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/objects.jpg"
# Select visual feature type(s) you want to focus on when analyzing an image
image_features = ['objects', 'tags']


#Auntheticate your credentials and create a client
subscription_key = "put_your_key_here"
endpoint = "put_endpoint_location_here"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Create bounding boxes

def drawRectangle(object, draw):
    rect = object.rectangle 
    left = rect.x
    right = left + rect.w
    top = rect.y
    bottom = top + rect.h
    coordinates = ((left, top), (right, bottom))
    draw.rectangle(coordinates, outline = 'red')

# Get the objects detected

def getObjects(results, draw):
    print('OBJECTS DETECTED:')
    if len(results.objects) == 0:
        print('No objects detected')
    else:
        for object in results.objects:
            print('object at location {}, {}, {}, {}'.format(
                object.rectangle.x, object.rectangle.x+ object.rectangle.w,
                object.rectangle.y, object.rectangle.y+ object.rectangle.h
            ))

            drawRectangle(object, draw)
        print()
        print('Bounding boxes drawn around objects, see popup')
    print()

# Prints the tag from the images

def getTags(results):
    #print results with confidence score
    print('TAGS:')
    if (len(results.tags) == 0):
        print('No tags detected')
    else:
        for tag in results.tags:
            print(" '{}' with confidence {:.2f}%".format(
                tag.name, tag.confidence*100
            ))
    print()

''' 
Analyze image
'''
print('Analyze local image')
print()

local_image_object = open(local_image, 'rb')
image_l = Image.open(local_image)
draw = ImageDraw.Draw(image_l)

results_local = computervision_client.analyze_image_in_stream(local_image_object, image_features)

getObjects(results_local, draw)
getTags(results_local)

image_l.show()
print()


'''
Detecting objects
'''

print('Analyze remote image')
print()

results_remote = computervision_client.analyze_image(remote_image, image_features)

#Download
object_image = requests.get(remote_image)
image_r = Image.open(BytesIO(object_image.content))
draw = ImageDraw.Draw(image_r)

#Show bounding boxes
getObjects(results_remote, draw)
getTags(results_remote)

image_r.show()