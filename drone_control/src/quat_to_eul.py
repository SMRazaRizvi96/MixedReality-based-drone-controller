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
    cube.orientation.x = currentcubePos.rot_x
    cube.orientation.y = currentcubePos.rot_y
    cube.orientation.z = currentcubePos.rot_z
    cube.orientation.w = currentcubePos.rot_w


"""
def telloPos(currenttelloPos):
    global tello
    tello.position.x = -currenttelloPos.QR_pos_z
    tello.position.y = currenttelloPos.QR_pos_x
    tello.position.z = currenttelloPos.QR_pos_y
    tello.orientation.x = -currenttelloPos.pos_z
    tello.orientation.y = currenttelloPos.pos_x
    tello.orientation.z = currenttelloPos.pos_y
    tello.orientation.w = currenttelloPos.pos_w

"""

"""
def quat_to_eul():
	euler_cube_rotation_list = [cube.orientation.x, cube.orientation.y, cube.orientation.z, cube.orientation.w]
	(roll, pitch, yaw) = euler_from_quaternion(euler_cube_rotation_list)
	print("Roll: ", roll*180/3.142, "Pitch: ", pitch*180/3.142, "Yaw: ", yaw*180/3.142)
	time.sleep(0.1)
	
"""

"""
def quat_to_eul():
        
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        

	x = cube.orientation.x
	y = cube.orientation.y
	z = cube.orientation.z
	w = cube.orientation.w

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        print('Roll: ', roll_x, 'Pitch: ', pitch_y, 'Yaw: ', yaw_z) # in radians
"""

def quat_to_eul():

	cube.position.x = -currentcubePos.pos_z
	cube.position.y = currentcubePos.pos_x
	cube.position.z = currentcubePos.pos_y
	cube.orientation.x = currentcubePos.rot_x
	cube.orientation.y = currentcubePos.rot_y
	cube.orientation.z = currentcubePos.rot_z
	cube.orientation.w = currentcubePos.rot_w



def main():

	rospy.init_node('Tello_Server')

	global cube, tello, sock, tello_address, goalPose, feedback
	cube = Pose()
	tello = Pose()
	goalPose = Pose()
	
	sub_cube = rospy.Subscriber("/target_pose", PosRot, cubePos)
	#sub_tello = rospy.Subscriber("/qr_code_pose", QRPose, telloPos)
	
	while(not rospy.is_shutdown()):
		quat_to_eul()
	
	rospy.spin()


if __name__ == '__main__':
    main()


