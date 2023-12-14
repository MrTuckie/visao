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

# Define the initial and final depth for drawing the epipolar line 
z_ini = 1
z_fim = 100

fig, axs = plt.subplots(1,2,figsize=(20,5))

while True:

	# Show images	
	plt.axes(axs[0])
	plt.imshow(imgL_rgb)
	
	plt.axes(axs[1])
	plt.imshow(imgR_rgb)
	fig.suptitle('Mark just uL', fontsize=16)
	
	# Select point in the left image
	point = plt.ginput(1)
	uL = point[0][0]
	v = point[0][1] 
	uL = np.around(uL)
	
	# Based on the selected point define the initial and final coordinates for the epipolar line in the second image
	# Draw the epipolar line and the initial and final points
	if uL <= w :
		u_ini = uL - b*f/z_ini
		u_ini = np.maximum(u_ini,0)
		u_fim = uL - b*f/z_fim
		u_fim = np.minimum(u_fim,(w-1))
		axs[0].plot(uL,v,'*b')
		axs[1].plot([u_ini,u_fim],[v,v],'-r',linewidth=2)
		axs[1].plot(u_ini,v,'*y')
		axs[1].plot(u_fim,v,'*c')

	plt.pause(0.5)
	
	


