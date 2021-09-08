#!/usr/bin/env python3

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
from drone_control.msg import TargetPose
from drone_control.msg import QRPose
from drone_control.msg import StatusColor
from visualization_msgs.msg import Marker


def hologramPos(currenthologramPos):
    global hologram
    hologram.position.x = currenthologramPos.pos_x
    hologram.position.y = currenthologramPos.pos_y
    hologram.position.z = currenthologramPos.pos_z

def telloPos(currenttelloPos):
    global tello
    tello.position.x = -currenttelloPos.position.x
    tello.position.y = currenttelloPos.position.y
    tello.position.z = currenttelloPos.position.z


def hologramTrack():
	
	global tello, hologram, pub_vel, drone_vel, goalPose, msg

	while(not rospy.is_shutdown() and 'stop' not in msg):
		try:
			if(tello):
				goalPose.position.x = 1*(hologram.position.x - tello.position.x)
				goalPose.position.y = 1*(hologram.position.y - tello.position.y)
				goalPose.position.z = 1*(hologram.position.z - tello.position.z)
				#print("Goal x: ", goalPose.position.x, " Goal y: ", goalPose.position.y, " Goal z: ", goalPose.position.z)

				drone_vel.linear.x = -goalPose.position.x
				drone_vel.linear.y = -goalPose.position.z
				drone_vel.linear.z = goalPose.position.y
				pub_vel.publish(drone_vel)
				tello = Pose()
				
			else:
				drone_vel.linear.x = 0
				drone_vel.linear.y = 0
				drone_vel.linear.z = 0
				pub_vel.publish(drone_vel)
		
		except KeyboardInterrupt:
			print ('\n . . .\n')
			
	drone_vel.linear.x = 0
	drone_vel.linear.y = 0
	drone_vel.linear.z = 0
	pub_vel.publish(drone_vel)
	
	return


def main():

	rospy.init_node('Tello_Server')

	global hologram, tello, goalPose, Marker, takeOff, pub_vel, drone_vel, msg
	hologram = Pose()
	tello = Pose()
	goalPose = Pose()
	takeOff = Empty()
	land = Empty()
	drone_vel = Twist()
	msg = ''
	
	sub_hologram = rospy.Subscriber("/target_pose", TargetPose, hologramPos)
	sub_tello = rospy.Subscriber("/tello/ArucoPose", Pose, telloPos)
	pub_takeOff = rospy.Publisher("/tello/takeoff", Empty, queue_size=10)
	pub_vel = rospy.Publisher("/tello/cmd_vel", Twist, queue_size=10)
	pub_land = rospy.Publisher("/tello/land", Empty, queue_size=10)


	while(not 'stop' in msg):
		print ("Please type 'takeoff' OR 'land' OR 'track' \n")
		msg = input("");

		if('takeoff' in msg):
			pub_takeOff.publish(takeOff)
			
		elif('land' in msg):
			pub_land.publish(land)
			
		elif('track' in msg):
			hologramTrack()
			msg = 'land'
			
		elif('up' in msg):
			drone_vel.linear.x = 0
			drone_vel.linear.y = 0
			drone_vel.linear.z = 1
			pub_vel.publish(drone_vel)
			
			time.sleep(0.5)
			drone_vel.linear.x = 0
			drone_vel.linear.y = 0
			drone_vel.linear.z = 0
			pub_vel.publish(drone_vel)
			
		elif('down' in msg):
			drone_vel.linear.x = 0
			drone_vel.linear.y = 0
			drone_vel.linear.z = -1
			pub_vel.publish(drone_vel)
			
			time.sleep(0.5)
			drone_vel.linear.x = 0
			drone_vel.linear.y = 0
			drone_vel.linear.z = 0
			pub_vel.publish(drone_vel)
			
		elif('forward' in msg):
			drone_vel.linear.x = 0
			drone_vel.linear.y = 1
			drone_vel.linear.z = 0
			pub_vel.publish(drone_vel)
			
			time.sleep(0.5)
			drone_vel.linear.x = 0
			drone_vel.linear.y = 0
			drone_vel.linear.z = 0
			pub_vel.publish(drone_vel)
			
		elif('back' in msg):
			drone_vel.linear.x = 0
			drone_vel.linear.y = -1
			drone_vel.linear.z = 0
			pub_vel.publish(drone_vel)
			
			time.sleep(0.5)
			drone_vel.linear.x = 0
			drone_vel.linear.y = 0
			drone_vel.linear.z = 0
			pub_vel.publish(drone_vel)
			
		elif('left' in msg):
			drone_vel.linear.x = -1
			drone_vel.linear.y = 0
			drone_vel.linear.z = 0
			pub_vel.publish(drone_vel)
			
			time.sleep(0.5)
			drone_vel.linear.x = 0
			drone_vel.linear.y = 0
			drone_vel.linear.z = 0
			pub_vel.publish(drone_vel)
			
		elif('right' in msg):
			drone_vel.linear.x = 1
			drone_vel.linear.y = 0
			drone_vel.linear.z = 0
			pub_vel.publish(drone_vel)
			
			time.sleep(0.5)
			drone_vel.linear.x = 0
			drone_vel.linear.y = 0
			drone_vel.linear.z = 0
			pub_vel.publish(drone_vel)
			

	pub_land.publish(land)
	time.sleep(3)
	return
	
	#rospy.spin()


if __name__ == '__main__':
    main()



