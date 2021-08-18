#!/usr/bin/env python

# Tello Python3 Control Demo 
#
# http://www.ryzerobotics.com/
#
# 1/1/2018

# This is a Server. TELLO has its own client.
# Type the commands, and it will send the UDP Packets to the UDP CLients.
# Problem to solve: Once ctrl-c from Track, you cannot type track again and go to Tracking

import threading 
import socket
import sys
import time
import platform  

# Python libs

import math
import random
import actionlib
import subprocess
import signal

# numpy and scipy
import numpy as np


# Ros libraries
import roslib
import rospy

# Ros Messages

from geometry_msgs.msg import Twist, Point, Pose
from std_msgs.msg import Empty
from std_msgs.msg import String
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from unity_robotics_demo_msgs.msg import PosRot
from unity_robotics_demo_msgs.msg import QRPose
from tf.transformations import euler_from_quaternion


def cubePos(currentcubePos):
    global cube
    #cube.position.x = -(currentcubePos.pos_z-0.5)
    cube.position.x = -currentcubePos.pos_z
    cube.position.y = currentcubePos.pos_x
    cube.position.z = currentcubePos.pos_y
    cube.orientation.x = -currentcubePos.pos_z
    cube.orientation.y = currentcubePos.pos_x
    cube.orientation.z = currentcubePos.pos_y
    cube.orientation.w = currentcubePos.pos_w


def telloPos(currenttelloPos):
    global tello
    tello.position.x = -currenttelloPos.QR_pos_z
    tello.position.y = currenttelloPos.QR_pos_x
    tello.position.z = currenttelloPos.QR_pos_y
    tello.orientation.x = -currenttelloPos.pos_z
    tello.orientation.y = currenttelloPos.pos_x
    tello.orientation.z = currenttelloPos.pos_y
    tello.orientation.w = currenttelloPos.pos_w

def quat_to_eul():
	euler_cube_rotation_list = [cube.orientation.x, cube.orientation.y, cube.orientation.z, cube.orientation.w]
	(roll, pitch, yaw) = euler_from_quaternion(euler_cube_rotation_list)
	print("Roll: ", roll, "Pitch: ", pitch, "Yaw: ", yaw)
	time.sleep(0.1)
	


def main():

	rospy.init_node('Tello_Server')

	global cube, tello, sock, tello_address, goalPose, feedback
	cube = Pose()
	tello = Pose()
	goalPose = Pose()
	
	sub_cube = rospy.Subscriber("/pos_rot", PosRot, cubePos)
	sub_tello = rospy.Subscriber("/qr_code_pose", QRPose, telloPos)
	
	while(cube):
		quat_to_eul()
	
	rospy.spin()


if __name__ == '__main__':
    main()


