import airsim
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import imutils

number_of_images = 30
IMAGEDIR = 'C:/IMAGES/'
try:
    os.stat(IMAGEDIR)
except:
    os.mkdir(IMAGEDIR)

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.takeoffAsync().join()
client.moveToPositionAsync(4, 14, -1, 5).join()

training_images = []

while True:
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(response.height, response.width, 3)
    training_images.append(img_rgb)

    if len(training_images)==number_of_images:
        for i in range(number_of_images):
            AirSimClientBase.write_file(os.path.normpath(IMAGEDIR + '/image%03d.png'  % i ), training_images[i])
            #below line for writing a single image from the camera to a directory
            #airsim.write_file(os.path.normpath('/temp/py1.png'), response.image_data_uint8)
        training_images.pop(0)

     #collision_info = client.getCollisionInfo()

    time.sleep(0.1)

client.enableApiControl(False)
