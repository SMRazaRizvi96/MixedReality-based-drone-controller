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
	global count, lastPose
	realMarker.id = newArPose.id
	count+=1
	
	if(realMarker.id == 1):
		realMarker.pose.position.x = ID1.x + newArPose.pose.position.x
		realMarker.pose.position.y = ID1.y + newArPose.pose.position.y
		realMarker.pose.position.z = ID1.z + newArPose.pose.position.z
		
	elif(realMarker.id == 10):
		realMarker.pose.position.x = ID10.x + newArPose.pose.position.x
		realMarker.pose.position.y = ID10.y + newArPose.pose.position.y
		realMarker.pose.position.z = ID10.z + newArPose.pose.position.z

	
	if(count < 5 and (abs(lastPose.position.x - realMarker.pose.position.x) < sensitivity and abs(lastPose.position.y - realMarker.pose.position.y) < sensitivity and abs(lastPose.position.z - realMarker.pose.position.z) < sensitivity)):
		average.pose.position.x = average.pose.position.x + realMarker.pose.position.x
		average.pose.position.y = average.pose.position.y + realMarker.pose.position.y
		average.pose.position.z = average.pose.position.z + realMarker.pose.position.z
	
	elif(count ==5):
		average.pose.position.x = average.pose.position.x/5
		average.pose.position.y = average.pose.position.y/5
		average.pose.position.z = average.pose.position.z/5	
		TelloPose.position = average.pose.position
		pub_tellopose.publish(TelloPose)
		count = 0
				
		print('Tello ID: ', realMarker.id,'\n')
		print('Tello Position x: ', realMarker.pose.position.x,'\n')
		print('Tello Code Position y: ', realMarker.pose.position.y,'\n')
		print('Tello Position z: ', realMarker.pose.position.z,'\n')
		
	lastPose= realMarker.pose
	
def main():

	rospy.init_node('tello_Aruco_Pose')
	
	global ID1, ID10, realMarker, TelloPose, pub_tellopose, lastPose, average, count, sensitivity

	sub_ArPose = rospy.Subscriber("/aruco_single/marker", Marker, AruCoPose)

	pub_tellopose = rospy.Publisher("/tello/ArucoPose", Pose,queue_size=10)
	
	TelloPose = Pose()
	lastPose = Pose()
	realMarker = Marker()
	average = Marker()
	ID1 = offsets()
	count = 0
	sensitivity = 0.3
	#ID1.x =0.525413
	#ID1.y =0.0017
	#ID1.z =-0.1676
	
	ID1.x =0.457503
	ID1.y =0.275907
	ID1.z =-0.37343
	
	ID10 = offsets()
	#ID10.x =1.0783
	#ID10.y =-0.000827
	#ID10.z =-0.2089
	
	ID10.x =1.1789
	ID10.y =0.198291
	ID10.z =-0.39814

	while(not rospy.is_shutdown()):
		a = 1
		#if(realMarker):
		#	TelloPose.position = realMarker.pose.position
		#	pub_tellopose.publish(TelloPose)
		
	rospy.spin()


if __name__ == '__main__':
    main()


