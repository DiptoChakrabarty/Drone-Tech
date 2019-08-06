# ready to run example: PythonClient/multirotor/hello_drone.py
import airsim
import numpy as np
import matplotlib.pyplot as plt

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Async methods returns Future. Call join() to wait for task to complete.
client.takeoffAsync().join()
client.moveToPositionAsync(-5, 10, -10, 5).join()

responses = client.simGetImages([airsim.ImageRequest("0",airsim.ImageType.DepthVis,False,False)])
response = responses[0]
img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)


#responses = client.simGetImages([ImageRequest("0", airsim.ImageType.Scene, False, False)])
#response = responses[0]

# reshape array to 4 channel image array H X W X 4

img_rgb = img1d.reshape(response.height, response.width, 3)
print(img_rgb.shape)
img = []
for x in img_rgb:
    img.append(img_rgb)
        for len in img:
            while True:
                plt.imshow(len)
                plt.show()'''
import cv2
import imutils

image=cv2.imread("figure_1.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
# compute the center of the contour

    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # draw the contour and center of the shape on the image
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120, 155, 85), 2)

    # show the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    #print(len(img))


#plt.imshow(img_rgb)
#plt.show()
