import airsim
import cv2
import numpy as np
import imutils
import math

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)
stacks=[]
print("Take Off man")
client.takeoffAsync().join()
target_dst= list(map(int,input().split()))
stacks.append(target_dst)
client.moveToPositionAsync(stacks[-1][0],stacks[-1][1],stacks[-1][2],14)
#client.moveToPositionAsync(0,0,0,10)
print("@@@@@@@@@@@@@@@@@@@@@@@@@@")

def euc_dist():
    p = ((stacks[-1][0]-stacks[0][0])**2+(stacks[-1][1]-stacks[0][1])**2+(stacks[-1][2]-stacks[0][2]))**(1/2)

    if len(stacks)==1:
        airsim.moveToPositionAsync(stacks[-1][0],stacks[-1][1],stacks[-1][2],14)
    if p == 0:
        break

while(True):


    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthVis, False, False)])
    response = responses[0]

    # get numpy array
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)

    # reshape array to 4 channel image array H X W X 4
    img_rgb = img1d.reshape(response.height, response.width, 3)

    # original image is fliped vertically
    image = np.flipud(img_rgb)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find Canny edges
    edged = cv2.Canny(gray, 30, 200)
    #cv2.waitKey(0)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    # Finding Contours
    # Use a copy of the image e.g. edged.copy()
    # since findContours alters the image
    contours, hierarchy = cv2.findContours(edged,
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

   # cv2.imshow('Canny Edges After Contouring', edged)
    #cv2.waitKey(0)

    print("Number of Contours found = " + str(len(contours)))

    # Draw all contours
    # -1 signifies drawing all contours
    cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    #print(cnts)
    m=0
    for c in cnts:
        #print(c)
        #print(len(c))
        #continue
        area=cv2.contourArea(c)
        print(area)
        if area>m:
            #print(c)
            m=area
            M = cv2.moments(c)
            cX = int(M["m10"] / (M["m00"] ))
            cY = int(M["m01"] / (M["m00"]))
        #print(len(c))
        # compute the center of the contour
            #print(cX,cY)

    color = np.array(image[cY][cX])
    cv2.circle(image, (int(cX), int(cY)), 5, (255, 0, 0), -1)
    #print(image[125][192]) # Let this distance be 2 m
    #print(image[110][116]) # Let this distance be 4 m
    def colorToDistance(color, slope = -0.02820855, constant = 7.03992702):
        # Simple Linear Regression
        return color*slope + constant
    def pixelToComponents(pixel, distance, heading = 0, currentLocation = (0,0,0), image_size = image.shape[:2], max_angleX = math.radians(90)):
        # heading = 0 means heading towards X axis, 90 means Y axis and so on
        # max_x / 2 is equal to heading angle. if this - x = 0, then X,Y = distance*cos(heading), distance*sin(heading)
        # AngleXY
        max_y, max_x = image_size
        x,y = pixel
        mid_x = max_x / 2
        mid_y = max_y / 2
        deltaAngle = ((x - mid_x) / max_x) * max_angleX
        angleXY = heading - deltaAngle
        angleZ = -((y - mid_y) / max_y) * max_angleX
        return np.multiply(distance, [math.cos(angleXY), math.sin(angleXY), math.sin(angleZ)])
    dis = colorToDistance(color)
    #print(dis)
    #print(pixelToComponents((cX,cY), dis))
    f_c=pixelToComponents((200, 194), dis)
    secondary_dest=[f_c[0],f_c[1], f_c[2], 14]
    stacks.append(secondary_dest)
    p = ((stacks[-1][0]-stacks[0][0])**2+(stacks[-1][1]-stacks[0][1])**2+(stacks[-1][2]-stacks[0][2]))**(1/2)
    if len(stacks)==1:
        airsim.moveToPositionAsync(stacks[-1][0],stacks[-1][1],stacks[-1][2],14)
    elif len(stacks)>1:
        client.moveToPositionAsync(stacks[-1][0],stacks[-1][1],stacks[-1][2],14)
        stacks.pop()
        if len(stacks)==1:
            airsim.moveToPositionAsync(stacks[-1][0],stacks[-1][1],stacks[-1][2],14)
    else:
        None
        #client.moveToPositionAsync(stacks[-1][0],stacks[-1][1],stacks[-1][2],14).join()
    if p == 0:
        break
#    stacks.pop()
