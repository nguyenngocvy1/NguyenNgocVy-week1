import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

### TASK 1 ###

def roundUp(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

# draw Rotated Rect bounding for drop
def drawBoundingRect(contour):
    # get the min area rect
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box) #convert all coordinates floating point value to int
    # draw all contours
    cv2.drawContours(img_draw, [box], 0, (0, 255, 0), 1)
#read image file.
open_path_fname = "C:\\MyFolder\\Code\\Python\\week1\\img\\week1.png"
img = cv2.imread(open_path_fname,2)
img_draw = cv2.imread(open_path_fname,1)
#more smoothing, make the image blur to avoid the noises.
#img_blur = cv2.GaussianBlur(img, (3,3), 0)
#Canny edge direction.
threshold = 0
edges = cv2.Canny(img, threshold, threshold*2)
# get contours list
contours, _ = cv2.findContours(
	edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#print number of drops
total = len(contours)
print("(Task 1)number of drops in the image : ", total)

diameter_list = []
for cnt in contours :
    drawBoundingRect(cnt)
#save as image.
save_path = "C:\\MyFolder\\Code\\Python\\week1\\img\\week1Task1result.png"
cv2.imwrite(save_path, img_draw)

#show image on display.
cv2.imshow("Bounding Rectangle of Drops", img_draw)
cv2.waitKey(0)
cv2.destroyAllWindows()

#### TASK 2 ###

#reset image file.
img_draw = cv2.imread(open_path_fname,1)

#draw black circle (find ROI).
height, width = img.shape
center = (int(width/2-120), int(height/2-350))
radius = 1391
black_circle = cv2.circle(img, center, radius, (0,0,0), -1 )

#Canny edge direction.
threshold = 0
edges = cv2.Canny(img, threshold, threshold*2)
#find contours.
contours, hierarchy = cv2.findContours(
	edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
total = len(contours)
print("(Task 2) number of drops in the image : ", total)
#find diameter
microns = 10 #10 microns per pixel
diameter_list = []
for cnt in contours :   
    drawBoundingRect(cnt)
    ((x,y),(width_rect,height_rect),angle)= cv2.minAreaRect(cnt)
    if width_rect < height_rect:
        diameter = width_rect*microns
    else:
        diameter = height_rect*microns
    diameter_list.append(diameter)

#find max diameter to use for loop
max_diameter = max(diameter_list)
print("max diameter:",max_diameter) #max diameter = 258.17

#data number/diameter of drops
size_num_drops = {}
# input data to num/diameter dict
count = 0
min_val = 0
for max_val in range(microns,int(roundUp(max_diameter,-1)+microns),microns):
    for diameter in diameter_list:
        if diameter >= min_val and diameter < max_val:
            count += 1
    size_num_drops[str(max_val)]=count
    count = 0
    min_val = max_val
#draw Diagram
size_drops = list(size_num_drops.keys())
num_drops = list(size_num_drops.values())
fig = plt.figure(figsize = (10, 5))
plt.bar(size_drops, num_drops, color = 'maroon',width =0.9)
plt.title('Distribute of drops')
plt.xlabel('Under size of drops')
plt.ylabel('Number of drops')
plt.show()

#save as image.
save_path = "C:\\MyFolder\\Code\\Python\\week1\\img\\week1Task2result.png"
cv2.imwrite(save_path, img_draw)

#show image on display.
cv2.imshow("Bounding Rectangle of Drops", img_draw)
cv2.waitKey(0)
cv2.destroyAllWindows()