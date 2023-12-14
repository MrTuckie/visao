# Initialization:
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import imutils
import scipy.io



# Images:
imgL = cv.imread('mineL.png')
imgL_rgb = cv.cvtColor(imgL, cv.COLOR_BGR2RGB)
imgL= cv.cvtColor(imgL,cv.COLOR_BGR2GRAY)
imgR = cv.imread('mineR.png')
imgR_rgb = cv.cvtColor(imgR, cv.COLOR_BGR2RGB)
imgR= cv.cvtColor(imgR,cv.COLOR_BGR2GRAY)
h,w = imgL.shape



# Camera Parameters
data = scipy.io.loadmat('class1_ex1.mat')

f = data['f'][0][0]
b = data['b'][0][0]
c0 = np.array([w/2,h/2]);
K = np.array([[f, 0, c0[0]],[0, f, c0[1]],[0, 0, 1]])
print(f)
print(b)
print(K)


## Example 1a:
# uL - uR = b*f/z
# z = b*f/(uL - uR)



fig, axs = plt.subplots(1,2,figsize=(20,10))
while True:
	
	# Show images
	plt.axes(axs[0])
	plt.imshow(imgL_rgb)
	plt.axes(axs[1])
	plt.imshow(imgR_rgb)
	
	fig.suptitle('Mark uL and uR', fontsize=16)

	# Select point in the left image
	axs[0].set_title('Mark uL')
	uL = plt.ginput(1)
	v = np.around(uL[0][1]) 
	uL = np.around(uL[0][0])
	axs[0].plot(uL,v,'*r')
	
	# Mark the correspondent point in the right image
	axs[1].set_title('Mark uR')
	uR = plt.ginput(1)
	v = np.around(uR[0][1]) 
	uR = np.around(uR[0][0])
	axs[1].plot(uR,v,'*r')
	
	# Calculate disparity and estimate the depth of that point in the 3D world
	z = b*f/np.abs(uL - uR)
	fig.suptitle('z = ' + str(z) +' blocos', fontsize=15,  color='red')
	
	plt.pause(2)


































