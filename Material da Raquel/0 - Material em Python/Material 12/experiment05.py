# Initialization:
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import imutils
import scipy.io




# Load images and data:

data = scipy.io.loadmat('class1_ex3.mat')

im1 = data['im1']
im2 = data['im2']
R21 = data ['R21']
t21 = data ['t21']
K = data['K']


## Defining projection centers
O1 = np.array([[0],[0],[0]])
O2 = np.dot(-R21.T,t21)


# Baseline
b = O2 - O1

# Define the transformations for rectifying the left and right images 
vx = (b/np.linalg.norm(b,2)).T
ax_z = np.array([0,0,1])
vy = np.cross(ax_z,vx)
vy = vy/np.linalg.norm(vy,2)
vz = np.cross(vx,vy)
vz = vz/np.linalg.norm(vz,2)

Rr1 = np.vstack((vx,vy,vz))

T1 = np.dot(np.dot(K,Rr1),np.linalg.inv(K))
T2 = np.dot(K,np.dot(Rr1,np.dot(R21.T,np.linalg.inv(K))))

# Rectify images
im3 = cv.warpPerspective(im1, T1, (im1.shape[1], im1.shape[0]))
im4 = cv.warpPerspective(im2, T2, (im2.shape[1], im2.shape[0]))

# Show original and rectified images
fig, axs = plt.subplots(2,2,figsize=(20,10))
 
plt.axes(axs[0,0])
plt.imshow(im1)
axs[0,0].set_title('Image 01', fontsize=12)

plt.axes(axs[0,1])
plt.imshow(im2)
axs[0,1].set_title('Image 02', fontsize=12)

plt.axes(axs[1,0])
plt.imshow(im3)
axs[1,0].set_title('Image 01 Rectified', fontsize=12)

plt.axes(axs[1,1])
plt.imshow(im4)
axs[1,1].set_title('Image 02 Rectified', fontsize=12)

plt.show()


# Select some data
h,w,ch = im1.shape
f = K[0,0]
b = np.linalg.norm(b,2)

# Draw the epipolar lines in the left and right images according to selected points
fig, axs = plt.subplots(1,2,figsize=(20,10))

while True:

	#plt.cla() 	
	plt.axes(axs[0])
	plt.imshow(im3)
	
	plt.axes(axs[1])
	plt.imshow(im4)
	fig.suptitle('Mark just uL', fontsize=16)
	
	point = plt.ginput(1)
	uL = point[0][0]
	v = point[0][1] 
	uL = np.around(uL)
	axs[0].plot(uL,v,'*b')
	axs[0].plot([0,w-1],[v,v],'-c',linewidth=2)
	axs[1].plot([0,w-1],[v,v],'-r',linewidth=2)


	plt.pause(0.5)






