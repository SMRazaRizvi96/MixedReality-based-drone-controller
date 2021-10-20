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
from sensor_msgs.msg import Image

#from aruco_msgs.msg import Marker
from visualization_msgs.msg import Marker


class offsets:
	def __init__(self):
		self.x= 0
		self.y= 0
		self.z= 0



def AruCoPose(newArPose):

	#global realMarker
	#realMarker = Marker()
	global count, lastPose, average
	realMarker.id = newArPose.id
	#average = Marker()
	
	if(realMarker.id == 1):
		realMarker.pose.position.x = newArPose.pose.position.x
		realMarker.pose.position.y = newArPose.pose.position.y
		realMarker.pose.position.z = newArPose.pose.position.z
	
	if(realMarker.id == 10):
		realMarker.pose.position.x = ID10.x + newArPose.pose.position.x
		realMarker.pose.position.y = ID10.y + newArPose.pose.position.y
		realMarker.pose.position.z = ID10.z + newArPose.pose.position.z
		
	elif(realMarker.id == 20):
		realMarker.pose.position.x = ID20.x + newArPose.pose.position.x
		realMarker.pose.position.y = ID20.y + newArPose.pose.position.y
		realMarker.pose.position.z = ID20.z + newArPose.pose.position.z
		
	elif(realMarker.id == 30):
		realMarker.pose.position.x = ID30.x + newArPose.pose.position.x
		realMarker.pose.position.y = ID30.y + newArPose.pose.position.y
		realMarker.pose.position.z = ID30.z + newArPose.pose.position.z


	realMarker.pose.position.x = ID1.x + realMarker.pose.position.x
	realMarker.pose.position.y = ID1.y + realMarker.pose.position.y
	realMarker.pose.position.z = ID1.z + realMarker.pose.position.z
	
	if(count < 5 and (abs(lastPose.position.x - realMarker.pose.position.x) < sensitivity and abs(lastPose.position.y - realMarker.pose.position.y) < sensitivity and abs(lastPose.position.z - realMarker.pose.position.z) < sensitivity)):
		average.pose.position.x = average.pose.position.x + realMarker.pose.position.x
		average.pose.position.y = average.pose.position.y + realMarker.pose.position.y
		average.pose.position.z = average.pose.position.z + realMarker.pose.position.z
		
		count+=1
	
	elif(count ==5):

		TelloPose.position.x = average.pose.position.x/5
		TelloPose.position.y = average.pose.position.y/5
		TelloPose.position.z = average.pose.position.z/5
		pub_tellopose.publish(TelloPose)
		average = Marker()
		count = 0
				
		
	lastPose.position.x= realMarker.pose.position.x
	lastPose.position.y= realMarker.pose.position.y
	lastPose.position.z= realMarker.pose.position.z
	
def main():

	rospy.init_node('tello_Aruco_Pose')
	
	global ID1, ID10, ID20, ID30, realMarker, TelloPose, pub_tellopose, lastPose, average, count, sensitivity

	sub_ArPose = rospy.Subscriber("/aruco_single/marker", Marker, AruCoPose)

	pub_tellopose = rospy.Publisher("/tello/ArucoPose", Pose,queue_size=10)
	
	TelloPose = Pose()
	lastPose = Pose()
	realMarker = Marker()
	average = Marker()
	ID1 = offsets()
	ID10 = offsets()
	ID20 = offsets()
	ID30 = offsets()
	count = 0
	sensitivity = 0.3
	
	#ID1.x =0.2741187 +0.1
	#ID1.y =0.932959 +0.1
	#ID1.z =-0.2280 -0.2
	
	ID1.x =0.51133 +0.1
	ID1.y =0.009959 +0.1+0.2
	ID1.z =-0.1715 -0.2
	
	ID10.x =0.685443
	ID10.y =0 +0.1
	ID10.z =0
	
	ID20.x =1.10445
	ID20.y =-0.42439 +0.1
	ID20.z =0
	
	ID30.x =0.327208 -0.1
	ID30.y =-0.42949 +0.1
	ID30.z =0

	while(not rospy.is_shutdown()):
		a = 1
		
	rospy.spin()


if __name__ == '__main__':
    main()


