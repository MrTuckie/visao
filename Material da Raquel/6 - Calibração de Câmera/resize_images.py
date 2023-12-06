import imutils 
import cv2
import numpy as np
import glob


# Read images for calibration
images = glob.glob('./26102023/*.JPG')
# Print the number of images to see if all of them were read
print('Number of images read: ', len(images))
count = 1
# Read images, detect the corners, refine to subpixel precision and plot the detected corners
for fname in images:
    # Read image and convert to grayscale
    
    img = cv2.imread(fname)
    imsize = img.shape
    if (imsize[1] < imsize[0]):
            img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
            
    img2 = imutils.resize(img,width=640)
    kernel = np.array([[0, -1, 0],[-1, 5,-1],[0, -1, 0]])
    #kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    image_sharp = cv2.filter2D(src=img2, ddepth=-1, kernel=kernel)
    cv2.imwrite(f'./imagens_calibracao_chessboard/{str(count)}.JPG',image_sharp)
    count +=1
    
