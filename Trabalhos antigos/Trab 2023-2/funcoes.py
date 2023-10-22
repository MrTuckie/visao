import numpy as np
import matplotlib.pyplot as plt
from math import pi,cos,sin


def move (dx,dy,dz):
    T = np.eye(4)
    T[0,-1] = dx
    T[1,-1] = dy
    T[2,-1] = dz
    return T



def z_rotation(angle):
    angle = float(angle)
    angle = angle*pi/180
    rotation_matrix=np.array([[cos(angle),-sin(angle),0,0],[sin(angle),cos(angle),0,0],[0,0,1,0],[0,0,0,1]])
    return rotation_matrix

def x_rotation(angle):
    angle = float(angle)
    angle = angle*pi/180
    rotation_matrix=np.array([[1,0,0,0],[0, cos(angle),-sin(angle),0],[0, sin(angle), cos(angle),0],[0,0,0,1]])
    return rotation_matrix

def y_rotation(angle):
    angle = float(angle)
    angle = angle*pi/180
    rotation_matrix=np.array([[cos(angle),0, sin(angle),0],[0,1,0,0],[-sin(angle), 0, cos(angle),0],[0,0,0,1]])
    return rotation_matrix


def set_plot(ax=None,figure = None,lim=[-2,2]):
    if figure ==None:
        figure = plt.figure(figsize=(8,8))
    if ax==None:
        ax = plt.axes(projection='3d')
    
    ax.set_title("camera referecnce")
    ax.set_xlim(lim)
    ax.set_xlabel("x axis")
    ax.set_ylim(lim)
    ax.set_ylabel("y axis")
    ax.set_zlim(lim)
    ax.set_zlabel("z axis")
    return ax

#adding quivers to the plot
def draw_arrows(point,base,axis,length=1.5):
    # The object base is a matrix, where each column represents the vector 
    # of one of the axis, written in homogeneous coordinates (ax,ay,az,0)
    

    # Plot vector of x-axis
    axis.quiver(point[0],point[1],point[2],base[0,0],base[1,0],base[2,0],color='red',pivot='tail',  length=length)
    # Plot vector of y-axis
    axis.quiver(point[0],point[1],point[2],base[0,1],base[1,1],base[2,1],color='green',pivot='tail',  length=length)
    # Plot vector of z-axis
    axis.quiver(point[0],point[1],point[2],base[0,2],base[1,2],base[2,2],color='blue',pivot='tail',  length=length)

    return axis 

def generate_cam_origin():
    # base vector values
    e1 = np.array([[1],[0],[0],[0]]) # X
    e2 = np.array([[0],[1],[0],[0]]) # Y
    e3 = np.array([[0],[0],[1],[0]]) # Z
    base = np.hstack((e1,e2,e3))

    #origin point
    point =np.array([[0],[0],[0],[1]])

    cam = np.hstack((base,point))
    return cam

def move_cam_to_initial_point(cam):
    Rx = x_rotation(-90)
    Rz = z_rotation(90)
    T = move(25,-5,6)
    M = np.dot(np.dot(T,Rz),Rx)
    cam  = np.dot(M,cam)
    return cam

def generate_house_origin():
    house = np.array([[0,         0,         0],
            [0,  -10.0000,         0],
            [0, -10.0000,   12.0000],
            [0,  -10.4000,   11.5000],
            [0,   -5.0000,   16.0000],
            [0,         0,   12.0000],
            [0,    0.5000,   11.4000],
            [0,         0,   12.0000],
            [0,         0,         0],
    [-12.0000,         0,         0],
    [-12.0000,   -5.0000,         0],
    [-12.0000,  -10.0000,         0],
            [0,  -10.0000,         0],
            [0,  -10.0000,   12.0000],
    [-12.0000,  -10.0000,   12.0000],
    [-12.0000,         0,   12.0000],
            [0,         0,   12.0000],
            [0,  -10.0000,   12.0000],
            [0,  -10.5000,   11.4000],
    [-12.0000,  -10.5000,   11.4000],
    [-12.0000,  -10.0000,   12.0000],
    [-12.0000,   -5.0000,   16.0000],
            [0,   -5.0000,   16.0000],
            [0,    0.5000,   11.4000],
    [-12.0000,    0.5000,   11.4000],
    [-12.0000,         0,   12.0000],
    [-12.0000,   -5.0000,   16.0000],
    [-12.0000,  -10.0000,   12.0000],
    [-12.0000,  -10.0000,         0],
    [-12.0000,   -5.0000,         0],
    [-12.0000,         0,         0],
    [-12.0000,         0,   12.0000],
    [-12.0000,         0,         0]])

    house = np.transpose(house)

    #add a vector of ones to the house matrix to represent the house in homogeneous coordinates
    house = np.vstack([house, np.ones(np.size(house,1))])
    return house

def generate_projection_matrix():
    return np.eye(3,4)

def generate_inv(matrix):
    return np.linalg.inv(matrix)

def np_dot(matrix1,matrix2):
    return np.dot(matrix1,matrix2)