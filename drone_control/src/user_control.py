#!/usr/bin/env python

# Python libs
import sys
import time
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
from std_msgs.msg import String
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry


def dronePos(currentPos):
    
    drone.position.x = currentPos.position.x
    drone.position.y = currentPos.position.y
    drone.position.z = currentPos.position.z
    #print("Drone x: ", drone.position.x, "Drone y: ", drone.position.y, "Drone z: ", drone.position.z)




def main():

	global pub_cmd_vel, vel, goal, drone
	vel = Twist()
	goal = Pose()
	drone = Pose()
	sub_odom = rospy.Subscriber("/drone/gt_pose", Pose, dronePos)

	pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

	rospy.init_node('drone_control')

	goal.position.x = input("Input goal x: ")
	goal.position.y = input("Input goal y: ")
	goal.position.z = input("Input goal z: ")

	while(not rospy.is_shutdown()):
		if(((goal.position.x - drone.position.x) > 0.2) & ((goal.position.y - drone.position.y) > 0.2) & ((goal.position.z - drone.position.z) > 0.2)):
			vel.linear.x = 2*(goal.position.x - drone.position.x)
			vel.linear.y = 2*(goal.position.y - drone.position.y)
			vel.linear.z = 2*(goal.position.z - drone.position.z)

		else:
			vel.linear.x = 0
			vel.linear.y = 0
			vel.linear.z = 0
		pub_cmd_vel.publish(vel)
	    	print("Drone x: ", drone.position.x, "Drone y: ", drone.position.y, "Drone z: ", drone.position.z)
		#print("Publishing")


	rospy.spin()


if __name__ == '__main__':
    main()







