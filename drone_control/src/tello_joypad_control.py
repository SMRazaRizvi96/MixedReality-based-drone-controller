#!/usr/bin/env python3

import threading 
import socket
import sys
import time
import platform  

from timeit import default_timer as timer
from datetime import timedelta

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
from sensor_msgs.msg import Joy
from nav_msgs.msg import Odometry
from drone_control.msg import TargetPose
from drone_control.msg import QRPose
from drone_control.msg import StatusColor
from visualization_msgs.msg import Marker
from tello_driver.msg import TelloStatus

def telloPos(currenttelloPos):
	global tello, flag
	tello.position.x = currenttelloPos.position.x
	tello.position.y = currenttelloPos.position.y
	tello.position.z = currenttelloPos.position.z
  
    
def joyStatus(joystat):
	joystick = joystat
	#print (abs(joystick.axes[0]))		
		
	# x vel

	if(tello.position.x < 0.2):	
		drone_vel.linear.x = -abs(joystick.axes[0])
		
	elif(tello.position.x > 2):
		drone_vel.linear.x = abs(joystick.axes[0])
		
	else:
		drone_vel.linear.x = joystick.axes[0]
		
		
	# y vel

	if(tello.position.z < 0.3):	
		drone_vel.linear.y = -abs(joystick.axes[1])
		
	elif(tello.position.z > 1.3):
		drone_vel.linear.y = abs(joystick.axes[1])
		
	else:
		drone_vel.linear.y = joystick.axes[1]
	
	# z vel
	if(tello.position.y < -0.6):
		drone_vel.linear.z = joystick.buttons[0]
		
	elif(tello.position.y > 0.3):
		drone_vel.linear.z = joystick.buttons[2]
		
	else:
		if(joystick.buttons[0]):
			drone_vel.linear.z = 1
		elif(joystick.buttons[2]):
			drone_vel.linear.z = -1
		else:
			drone_vel.linear.z = 0
		
	pub_vel.publish(drone_vel)
	
	if(joystick.buttons[5]):
		pub_takeOff.publish(takeOff)
		print("Takeoff")
		
	elif(joystick.buttons[7]):
		pub_land.publish(land)
		print("Land")
		
	
def telloStat(newStatus):
    global telloStatus
    telloStatus = newStatus
    

def JoyTrack():

	if(not rospy.is_shutdown()):
		print(joystick.axes[0])
	
	return


def main():

	rospy.init_node('tello_joypad_control')

	global hologram, tello, goalPose, Marker, takeOff, pub_vel, drone_vel, zero_vel, msg, telloStatus, ID1, ID10, realMarker, pub_tellopose, speed, flag, integral_x, integral_y, integral_z, holo_counter_x, holo_counter_y, holo_counter_z, i, holoCount, counter, waitNext, dataFile, y_integral_sum, joystick, pub_land, pub_takeOff, land
		
	hologram = Pose()
	tello = Pose()
	goalPose = Pose()
	takeOff = Empty()
	land = Empty()
	drone_vel = Twist()
	zero_vel = Twist()
	telloStatus = TelloStatus()
	realMarker = Marker()
	joystick = Joy()
	
	#integral_x = []
	#integral_y = []
	#integral_z = []
	
	holo_counter_x = []
	holo_counter_y = []
	holo_counter_z = []
	
	holoCount = 0
	waitNext = 0
	
	msg = ''
	speed =1
	flag = 1
	i = 0
	counter = 0
	y_integral_sum = 0

	
	# Subscribed Topics
	#sub_hologram = rospy.Subscriber("/target_pose", TargetPose, hologramPos)
	sub_tello = rospy.Subscriber("/tello/ArucoPose", Pose, telloPos)
	sub_tello_status = rospy.Subscriber("/tello/status", TelloStatus, telloStat)
	sub_joy = rospy.Subscriber("/joy", Joy, joyStatus)
	
	
	# Published Topics
	pub_takeOff = rospy.Publisher("/tello/takeoff", Empty, queue_size=10)
	pub_vel = rospy.Publisher("/tello/cmd_vel", Twist, queue_size=10)
	pub_land = rospy.Publisher("/tello/land", Empty, queue_size=10)
	
	zero_vel.linear.x = 0
	zero_vel.linear.y = 0
	zero_vel.linear.z = 0


	while(not rospy.is_shutdown()):
		#JoyTrack()
		a=1
	
	return
	
	#rospy.spin()


if __name__ == '__main__':
    main()



