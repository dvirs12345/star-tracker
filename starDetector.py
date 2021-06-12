import numpy as np
import argparse
import cv2
import math


# if you want to read from CMD
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", help = "path to the image file")
# args = vars(ap.parse_args())
# image = cv2.imread('fullExStarS9.jpg')


def takeRadius(elem):
    return float(elem[2])


def takeX(elem):
    return float(elem[0])


# file_name='/Users/revital/Downloads/120.png'
file_name = 'pic3.jpg'

file = open("%s_res.txt" % file_name, "w")
image = cv2.imread(file_name)
orig = image.copy()
imgheight, imgwidth = image.shape[:2]
# image = image[0:2500,0:4000 ]
# orig = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
# sobelx = cv2.Sobel(image,cv2.CV_64F,1,0,ksize=11)
# sobelx=sobelx*255
edges = cv2.Canny(image, 70, 100)
print(np.max(edges))
print((edges.sum() / 255) / (imgheight * imgwidth))

# print(edges)
# print (edges)
# cv2.circle(edges, maxLoc, 5, (255, 0, 0), 3)
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# print (contours)
contour_list = []
# print (contours)
# 0area = cv2.contourArea(contours[0])
res = []
for contour in contours:
    # approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    # print("in for")
    area = cv2.contourArea(contour)
    # print(area)
    (x, y), radius = cv2.minEnclosingCircle(contour)

    center = (int(x), int(y))
    radius = int(radius)
    xint = center[0]
    yint = center[1]
    x = str(x)
    y = str(y)
    r = str(radius)

    if 1 < radius < 5:  # (and xint>300 and yint> 300):
        cv2.circle(orig, center, radius + 4, (0, 255, 255), 5)
        res.append([x, y, radius])
# contour_list.append(contour)
# ret, thresh = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
connectivity = 4
# output = cv2.connectedComponentsWithStats(image, connectivity, cv2.CV_32S)
# cv2.drawContours(image, contour_list,  -1, (255,255,0), 1)
# display the results of the naive attempt
cv2.imshow("Naive", orig)
cv2.imwrite("%s_processed.jpg" % file_name, orig)

# res.sort(key=takeRadius,reverse=True )
res.sort(key=takeX, reverse=False)
# cv2.waitKey(0)
counter = 0
final_res = []
print(res)
file.write("%s ,%s ,%s \n" % (res[0][0], res[0][1], res[0][2]))
final_res.append([float(res[0][0]), float(res[0][1])])
for i in range(1, len(res)):
    if counter < 10 and math.fabs(float(res[i][0]) - float(res[i - 1][0])) > 10:
        file.write("%s ,%s ,%s \n" % (res[i][0], res[i][1], res[i][2]))
        final_res.append([float(res[i][0]), float(res[i][1])])
        counter = counter + 1

        # file.write(t)
    # file.write('\n')
file.close()

for i in range(len(final_res)):
    for j in range(i + 1, len(final_res)):
        x = final_res[i][0] - final_res[j][0]
        y = final_res[i][1] - final_res[j][1]
        d = math.sqrt(x * x + y * y)
        print(str(d))
