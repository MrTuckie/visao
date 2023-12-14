# Initialization:
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import imutils
import scipy.io



# Three different metrics for comparing the pixels inside a window for matching
# ZSAD (1), ZSSD (2) e NCC (3)
def matching(u2ini,u2end,W1,I2,dw,metric) :

	# line (v) and window size (dw)
	v = int(np.around(u2ini[1]))
	dw = int(dw)

	# Inicialization
	u2k_best = int(u2end[0])
	u2iniR = int(np.around(u2ini[0]))
	u2endR = int(np.around(u2end[0]))
	difference = np.zeros(u2endR-u2iniR)

	# Normalization of the window W1 using its mean
	W1_mean = np.mean(W1)
	W1 = W1 - W1_mean

	# ZSAD
	if (metric==1) :
		diff_best = 10000
		for u2k in range(u2iniR,u2endR):
			# Normalization of the pixel window in the second image
			W2 = I2[v-dw:v+dw,u2k-dw:u2k+dw,:]
			W2_mean = np.mean(W2)
			W2 = W2 - W2_mean
			# Calculate ZSAD - Zero Mean Sum of the absolute differences
			differenceW = np.abs(W1-W2)
			difference[u2k-u2iniR] = np.sum(differenceW)
			# Select the best match			
			if(difference[u2k-u2iniR]<diff_best):
				diff_best = difference[u2k-u2iniR]
				u2k_best = u2k
	#ZSSD			
	if(metric==2):
		diff_best = 10000
		for u2k in range(u2iniR,u2endR):
			# Normalization of the pixel window in the second image
			W2 = I2[v-dw:v+dw,u2k-dw:u2k+dw,:]
			W2_mean = np.mean(W2)
			W2 = W2 - W2_mean
			# Calculate ZSSD - Zero Mean Sum of the square differences
			differenceW = (W1-W2)**2
			# Took the square root just to reduce the value and compare with the threshold diff_best
			difference[u2k-u2iniR] = np.sqrt(np.sum(differenceW))
			# Select the best match
			if(difference[u2k-u2iniR]<diff_best):
				diff_best = difference[u2k-u2iniR]
				u2k_best = u2k
  
	#NCC
	if (metric==3):
		diff_best = 0
		for u2k in range(u2iniR,u2endR):
			# Normalization of the pixel window in the second image
			W2 = I2[v-dw:v+dw,u2k-dw:u2k+dw,:]
			W2_mean = np.mean(W2)
			W2 = W2 - W2_mean
			# Calculate NCC - Normalized Cross Correlation
			num = np.multiply(W1,W2)
			num = np.sum(num)
			den = np.sqrt(np.sum(W2**2)*np.sum(W1**2))
			if (num>den):
				nccW = 0
			else:
				nccW = num/den
			
			difference[u2k-u2iniR] = nccW
			# Select the best match
			if(difference[u2k-u2iniR]>diff_best):
				diff_best = difference[u2k-u2iniR]
				u2k_best = u2k
		
       
		
	# Select the pixel in the second image that correspon to the best match
	u2k_best_cont = u2ini[0] + ((u2k_best - u2iniR)*((u2end[0] - u2ini[0])/(u2endR - u2iniR)))

	u2 = np.array([u2k_best_cont,v,1])
	
	# Plot the metric variation along the epipolar line
	fig2, ax2 = plt.subplots()
	ax2.plot(np.arange(u2iniR,u2endR),difference)
	fig2.suptitle('Metric value = ' + str(diff_best), fontsize=13)

	
	return u2



###########  Main  ######################

# Images:
imgL = cv.imread('mineL.png')
imgL_rgb = cv.cvtColor(imgL, cv.COLOR_BGR2RGB)
imgL= cv.cvtColor(imgL,cv.COLOR_BGR2GRAY)
imgR = cv.imread('mineR.png')
imgR_rgb = cv.cvtColor(imgR, cv.COLOR_BGR2RGB)
imgR= cv.cvtColor(imgR,cv.COLOR_BGR2GRAY)
h,w = imgL.shape

# Show images
fig0a = plt.figure(1,figsize=(15,15))
ax0a = fig0a.add_subplot(111)
plt.imshow(imgL_rgb)
fig0a.show()
fig0b = plt.figure(2,figsize=(15,15))
ax0b = fig0b.add_subplot(111)
plt.imshow(imgR_rgb)
fig0b.show()


# Camera Parameters
data = scipy.io.loadmat('class1_ex1.mat')

f = data['f'][0][0]
b = data['b'][0][0]
c0 = np.array([w/2,h/2]);
K = np.array([[f, 0, c0[0]],[0, f, c0[1]],[0, 0, 1]])


# Define the initial and final depth for drawing the epipolar line 
z_ini = 1
z_fim = 500

# Define the window size for matching features
ws = 11
dw = (ws-1)/2
dw = int(dw)


ax0a.set_title('Left Image: Mark a point uL', fontsize=16)
plt.draw()
ax0b.set_title('Right Image', fontsize=16)
plt.draw()
	
	
# Select point in the left image
plt.figure(1)
point = plt.ginput(1)
uL = point[0][0]
vL = point[0][1] 
uL = int(np.around(uL))
vL = int(np.around(vL))

# Show image window around the selected pixel
fig1, ax1 = plt.subplots()
plt.imshow(imgL_rgb[vL-dw:vL+dw,uL-dw:uL+dw,:])
ax1.set_title('Window in the left image', fontsize=12)
plt.draw()

# Initialize column values for searching the correspondent point in the second image
u_ini = uL - b*f/z_ini
u_ini = np.maximum(u_ini,dw)
u_fim = uL - b*f/z_fim
u_fim = np.minimum(u_fim,(w-dw))

# Plot selected point in the left image and the epipolar line in the right image
ax0a.plot(uL,vL,'*b')
ax0b.plot([u_ini,u_fim],[vL,vL],'-r',linewidth=2)
ax0b.plot(u_ini,vL,'*y')
ax0b.plot(u_fim,vL,'*c')
plt.draw()

# Call the matching function to go through the epipolar line comparing windows and to find the correspondent point in the other image
u2 = matching(np.array([u_ini,vL,1]),np.array([u_fim,vL,1]),imgL_rgb[vL-dw:vL+dw,uL-dw:uL+dw,:],imgR_rgb,dw,2)

# Show the correspondent image window found in the other image
fig3, ax3 = plt.subplots()
plt.imshow(imgR_rgb[int(u2[1])-dw:int(u2[1])+dw,int(u2[0])-dw:int(u2[0])+dw,:])
# Plot the correspondent point in the other image
ax0b.plot(int(u2[0]),int(u2[1]),'oc')

## Calculate depth:
# uL - uR = b*f/z
# z = b*f/(uL - uR)
z = b*f/(uL - u2[0])
fig3.suptitle('Window in the right image \n'+ 'z = ' + str(z) + 'blocks', fontsize=12)

plt.draw()

plt.show()


























