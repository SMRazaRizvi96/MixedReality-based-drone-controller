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
    global hologram, holoCount
    hologram.position.x = currenthologramPos.pos_x
    hologram.position.y = currenthologramPos.pos_y
    hologram.position.z = currenthologramPos.pos_z
    
    holo_counter_x.append(hologram.position.x)


def telloPos(currenttelloPos):
	global tello, flag
	tello.position.x = currenttelloPos.position.x
	tello.position.y = currenttelloPos.position.y
	tello.position.z = currenttelloPos.position.z

	if('track' in msg and flag):
		 track_thread = threading.Thread(target=hologramTrack)
		 flag = 0
		 track_thread.start()
    
       
def telloStat(newStatus):
    global telloStatus
    telloStatus = newStatus
    

def hologramTrack():
	
	global tello, hologram, pub_vel, drone_vel, goalPose, msg, flag, i, counter, waitNext, y_integral_sum


	if(not rospy.is_shutdown() and 'stop' not in msg):
	
		goalPose.position.x = hologram.position.x - tello.position.x
		goalPose.position.y = hologram.position.y - tello.position.y
		goalPose.position.z = hologram.position.z - tello.position.z
		#print("\nGoal x: ", goalPose.position.x, " Goal y: ", goalPose.position.y, " Goal z: ", goalPose.position.z)
		
		y_integral_sum = y_integral_sum + goalPose.position.y

		
		if((not waitNext) and holo_counter_x[len(holo_counter_x)-2] == holo_counter_x[len(holo_counter_x)-1] and ((abs(goalPose.position.x) > 0.1) or (abs(goalPose.position.y) > 0.1) or (abs(goalPose.position.z) > 0.1))):
			counter = timer()
			i+=1
			
			st = "Goal ",i,  " Given: ", " x: ", hologram.position.x, "y: ", hologram.position.y, "z: ", hologram.position.z
			print(st , "\n")
			dataFile.write(str(st) + '\n')
			
			waitNext = 1
			
			
		if(waitNext and (abs(goalPose.position.x) <= 0.10) and (abs(goalPose.position.y) <= 0.10) and (abs(goalPose.position.z) <= 0.10)):
			timeElapsed = timer() - counter
			
			st = "Tello Pose: ", "x: ", tello.position.x, " y: ", tello.position.y, " z: ", tello.position.z
			print (st, "\n")
			dataFile.write(str(st) + '\n')
			st = "Time taken to reach the Goal: ", timedelta(seconds=timeElapsed)
			print (st, "\n")
			dataFile.write(str(st) + '\n')
			
			#holo_counter_x.clear()
			#holo_counter_y.clear()
			#holo_counter_z.clear()
			waitNext = 0
			
			
		# For the bounding box
		#if(not (0.2 < hologram.position.x < 2)):
		if(not (0.4 < hologram.position.x < 1.6)):
			goalPose.position.x = 0
			print ('Goal x outside bounding box')
			
		#if(not (-0.6 < hologram.position.y < 0.3)):
		if(not (-0.4 < hologram.position.y < 0.6)):
			goalPose.position.y = 0
			print ('Goal y outside bounding box')
			
		#if(not (0.3 < hologram.position.z < 1.3)):
		if(not (0.8 < hologram.position.z < 2.0)):
			goalPose.position.z = 0
			print ('Goal z outside bounding box')
		
		drone_vel.linear.x = -(speed)*goalPose.position.x #+ 0.01*(sum(integral_x))
		drone_vel.linear.y = -(speed)*goalPose.position.z #+ 0.02*(sum(integral_z))
		drone_vel.linear.z = (speed+0.5)*goalPose.position.y + 0.03*(y_integral_sum)
		pub_vel.publish(drone_vel)

		time.sleep(1)
		pub_vel.publish(zero_vel)
			
	pub_vel.publish(zero_vel)
	flag = 1
	
	return


def main():

	rospy.init_node('Tello_Server')

	global hologram, tello, goalPose, Marker, takeOff, pub_vel, drone_vel, zero_vel, msg, telloStatus, ID1, ID10, realMarker, pub_tellopose, speed, flag, integral_x, integral_y, integral_z, holo_counter_x, holo_counter_y, holo_counter_z, i, holoCount, counter, waitNext, dataFile, y_integral_sum, saveTello
	
	dataFile = open('datafile.txt','a')
	dataFile.write('\n')
	dataFile.write('New Data ---------------------------------------------------------\n')
	
	hologram = Pose()
	tello = Pose()
	saveTello = Pose()
	goalPose = Pose()
	takeOff = Empty()
	land = Empty()
	drone_vel = Twist()
	zero_vel = Twist()
	telloStatus = TelloStatus()
	realMarker = Marker()
	
	
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
	sub_hologram = rospy.Subscriber("/target_pose", TargetPose, hologramPos)
	sub_tello = rospy.Subscriber("/tello/ArucoPose", Pose, telloPos)
	sub_tello_status = rospy.Subscriber("/tello/status", TelloStatus, telloStat)
	
	
	# Published Topics
	pub_takeOff = rospy.Publisher("/tello/takeoff", Empty, queue_size=10)
	pub_vel = rospy.Publisher("/tello/cmd_vel", Twist, queue_size=10)
	pub_land = rospy.Publisher("/tello/land", Empty, queue_size=10)
	#pub_tellopose = rospy.Publisher("/tello/ArucoPose", Pose,queue_size=10)
	
	zero_vel.linear.x = 0
	zero_vel.linear.y = 0
	zero_vel.linear.z = 0


	while(not 'stop' in msg and not rospy.is_shutdown()):
		#print ("\nPlease type 'takeoff' OR 'land' OR 'track' OR 'stop' \n")
		print ("\nYou can type the following commands:\n\ntakeoff\nland\nup\ndown\nleft\nright\nforward\nback\ntrack\nstop\n")
		msg = input("");

		if('takeoff' in msg):
			pub_takeOff.publish(takeOff)
			print("Tello has taken off")
			
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
	
	print("Tello has landed safely")
	return
	
	#rospy.spin()


if __name__ == '__main__':
    main()



