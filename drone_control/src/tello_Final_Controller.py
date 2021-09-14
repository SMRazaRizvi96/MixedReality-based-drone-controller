#!/usr/bin/env python3

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
from tello_driver.msg import TelloStatus


class offsets:
	def __init__(self):
		self.x= 0
		self.y= 0
		self.z= 0


def hologramPos(currenthologramPos):
    global hologram
    hologram.position.x = currenthologramPos.pos_x
    hologram.position.y = currenthologramPos.pos_y
    hologram.position.z = currenthologramPos.pos_z

def telloPos(currenttelloPos):
	global tello
	tello.position.x = currenttelloPos.position.x
	tello.position.y = currenttelloPos.position.y
	tello.position.z = currenttelloPos.position.z

	if('track' in msg):
		 track_thread = threading.Thread(target=hologramTrack)
		 track_thread.start()
    
       
def telloStat(newStatus):
    global telloStatus
    telloStatus = newStatus
    

def hologramTrack():
	
	global tello, hologram, pub_vel, drone_vel, goalPose, msg


	if(not rospy.is_shutdown() and 'stop' not in msg):
	
		goalPose.position.x = hologram.position.x - tello.position.x
		goalPose.position.y = hologram.position.y - tello.position.y
		goalPose.position.z = hologram.position.z - tello.position.z
		print("\nGoal x: ", goalPose.position.x, " Goal y: ", goalPose.position.y, " Goal z: ", goalPose.position.z)
			
		#if(abs(goalPose.position.x) <= 0.1):
		#	goalPose.position.x = 0
			
		#if(abs(goalPose.position.y) <= 0.1):
		#	goalPose.position.y = 0
			
		#if(abs(goalPose.position.z) <= 0.1):
		#	goalPose.position.z = 0
			
			
		drone_vel.linear.x = -(speed)*goalPose.position.x
		drone_vel.linear.y = -(speed)*goalPose.position.z
		drone_vel.linear.z = (speed + 0.3)*goalPose.position.y
		pub_vel.publish(drone_vel)
		print('\nX Vel: ',drone_vel.linear.x, 'Y Vel: ',drone_vel.linear.y, 'Z Vel: ',drone_vel.linear.z)
		#time.sleep(0.5)
		time.sleep(0.4)
		#pub_vel.publish(zero_vel)
		flag = 0
			
	drone_vel.linear.x = 0
	drone_vel.linear.y = 0
	drone_vel.linear.z = 0
	pub_vel.publish(drone_vel)
	
	return


def main():

	rospy.init_node('Tello_Server')

	global hologram, tello, goalPose, Marker, takeOff, pub_vel, drone_vel, zero_vel, msg, telloStatus, ID1, ID10, realMarker, pub_tellopose, speed
	hologram = Pose()
	tello = Pose()
	goalPose = Pose()
	takeOff = Empty()
	land = Empty()
	drone_vel = Twist()
	zero_vel = Twist()
	telloStatus = TelloStatus()
	realMarker = Marker()
	msg = ''
	speed =1.2
	
	# Subscribed Topics
	sub_hologram = rospy.Subscriber("/target_pose", TargetPose, hologramPos)
	sub_tello = rospy.Subscriber("/tello/ArucoPose", Pose, telloPos)
	#sub_ArPose = rospy.Subscriber("/aruco_single/marker", Marker, telloPose)
	sub_tello_status = rospy.Subscriber("/tello/status", TelloStatus, telloStat)
	
	
	# Published Topics
	pub_takeOff = rospy.Publisher("/tello/takeoff", Empty, queue_size=10)
	pub_vel = rospy.Publisher("/tello/cmd_vel", Twist, queue_size=10)
	pub_land = rospy.Publisher("/tello/land", Empty, queue_size=10)
	pub_tellopose = rospy.Publisher("/tello/ArucoPose", Pose,queue_size=10)
	
	zero_vel.linear.x = 0
	zero_vel.linear.y = 0
	zero_vel.linear.z = 0


	while(not 'stop' in msg and not rospy.is_shutdown()):
		print ("\nPlease type 'takeoff' OR 'land' OR 'track' OR 'stop' \n")
		msg = input("");

		if('takeoff' in msg):
			pub_takeOff.publish(takeOff)
			
		elif('land' in msg):
			pub_land.publish(land)
			break
			
		#elif('track' in msg):
			#hologramTrack()
			#msg = 'land'
			
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
			
			
	drone_vel.linear.x = 0
	drone_vel.linear.y = 0
	drone_vel.linear.z = 0
	pub_vel.publish(drone_vel)
	
	while(telloStatus.is_flying):
		pub_land.publish(land)
		time.sleep(2)
	
	print("Tello has Landed")
	return
	
	#rospy.spin()


if __name__ == '__main__':
    main()



