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
	realMarker.id = newArPose.id
	
	if(realMarker.id == 1):
		realMarker.pose.position.x = ID1.x + newArPose.pose.position.x
		realMarker.pose.position.y = ID1.y + newArPose.pose.position.y
		realMarker.pose.position.z = ID1.z + newArPose.pose.position.z
		
	elif(realMarker.id == 10):
		realMarker.pose.position.x = ID10.x + newArPose.pose.position.x
		realMarker.pose.position.y = ID10.y + newArPose.pose.position.y
		realMarker.pose.position.z = ID10.z + newArPose.pose.position.z
		
	TelloPose.position = realMarker.pose.position
	pub_tellopose.publish(TelloPose)
			
	print('Tello ID: ', realMarker.id,'\n')
	print('Tello Position x: ', realMarker.pose.position.x,'\n')
	print('Tello Code Position y: ', realMarker.pose.position.y,'\n')
	print('Tello Position z: ', realMarker.pose.position.z,'\n')
	
def main():

	rospy.init_node('Tello_AruCo_Pose')
	
	global ID1, ID10, realMarker, TelloPose, pub_tellopose

	sub_ArPose = rospy.Subscriber("/aruco_single/marker", Marker, AruCoPose)

	pub_tellopose = rospy.Publisher("/tello/ArucoPose", Pose,queue_size=10)
	
	TelloPose = Pose()
	realMarker = Marker()
	ID1 = offsets()
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


