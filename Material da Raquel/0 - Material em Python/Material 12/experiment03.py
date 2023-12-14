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


## Example 1b:
# uL - uR = b*f/z
# z = b*f/(uL - uR)


# Select points in the left and right images to define segments and calculate their length in the 3D world
 
fig, axs = plt.subplots(1,2,figsize=(20,5))

while True:

	# Show images 	
	plt.axes(axs[0])
	plt.imshow(imgL_rgb)
	
	plt.axes(axs[1])
	plt.imshow(imgR_rgb)
	fig.suptitle('Mark two points on the left Image', fontsize=16)
	
	# Select first point in the left image
	point = plt.ginput(1)
	uL1 = np.around(point[0][0])
	vL1 = np.around(point[0][1]) 
	ptL1 = np.array([uL1, vL1,1])
	axs[0].plot(uL1,vL1,'*b')
	
	
	# Select second point in the left image
	point = plt.ginput(1)
	uL2 = np.around(point[0][0])
	vL2 = np.around(point[0][1]) 
	ptL2 = np.array([uL2, vL2,1])
	axs[0].plot([uL1,uL2],[vL1, vL2],'-*b',linewidth=2)
	
	plt.pause(0.5)
	fig.suptitle('Now mark the two correspondent points on the right Image', fontsize=16)
	
	# Select first point in the right image
	point = plt.ginput(1)
	uR1 = np.around(point[0][0])
	vR1 = np.around(point[0][1]) 
	ptR1 = np.array([uR1, vR1,1])
	axs[1].plot(uR1,vR1,'*b')
	
	# Select second point in the right image
	point = plt.ginput(1)
	uR2 = np.around(point[0][0])
	vR2 = np.around(point[0][1]) 
	ptR2 = np.array([uR2, vR2,1])
	axs[1].plot([uR1,uR2],[vR1, vR2],'-*b',linewidth=2)
	
	# Calculate the 3D length of the selected segment
	z1 = b*f/np.abs(uL1 - uR1)
	X1L = z1*np.dot(np.linalg.inv(K),ptL1)
	z2 = b*f/np.abs(uL2- uR2)
	X2L = z2*np.dot(np.linalg.inv(K),ptL2)
	d = np.linalg.norm(X1L-X2L,2)
	
	fig.suptitle('distance = '+ str(d) + ' blocos', fontsize=15,  color='red');
	
	
	plt.pause(1)
	
	


