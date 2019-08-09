# ready to run example: PythonClient/multirotor/hello_drone.py
import airsim
import numpy as np
import matplotlib.pyplot as plt
import cv2
import imutils

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Async methods returns Future. Call join() to wait for task to complete.
client.takeoffAsync().join()
client.moveToPositionAsync(4, 14, -1, 5).join()
responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
response = responses[0]
# reshape array to 4 channel image array H X W X 4
#img_rgb = img1d.reshape(response.height, response.width, 3)
#responses = client.simGetImages([airsim.ImageRequest("0",airsim.ImageType.DepthVis,False,False)])
#response = responses[0]
img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
img_rgb = img1d.reshape(response.height, response.width, 3)

def move(img_rgb):
    image=img_rgb
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
    # compute the center of the contour
        M = cv2.moments(c)
        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        except Exception:
            None
        l = [cX,cY]
        return l
count = 0
while(count<30):
    count=count+1
    #ret, frame = cap.read()
    c=move(img_rgb)
    cx,cy = c[0],c[1]
    client.moveToPositionAsync(cx, cy, -10, 5).join()
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(response.height, response.width, 3)



        # draw the contour and center of the shape on the image
        # show the image

    #print(len(img))
