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
from std_msgs.msg import Empty
from std_msgs.msg import String
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from unity_robotics_demo_msgs.msg import PosRot



def dronePos(currentPos):
    
    drone.position.x = currentPos.position.x
    drone.position.y = currentPos.position.y
    drone.position.z = currentPos.position.z
    #print("Drone x: ", drone.position.x, "Drone y: ", drone.position.y, "Drone z: ", drone.position.z)



def cubePos(currentcubePos):
    
    cube.position.x = 10*currentcubePos.pos_x
    cube.position.y = 10*currentcubePos.pos_y
    cube.position.z = 10*currentcubePos.pos_z
    #print("Cube x: ", cube.position.x, "Drone y: ", cube.position.y, "Drone z: ", cube.position.z)




def main():

	global pub_cmd_vel, pub_takeoff, vel, goal, drone, cube, empty, a
	vel = Twist()
	goal = Pose()
	drone = Pose()
	cube = Pose()
	empty = Empty()
	#empty = ""

	rospy.init_node('drone_control_from_cube')

	sub_odom = rospy.Subscriber("/drone/gt_pose", Pose, dronePos)
	sub_cube = rospy.Subscriber("/pos_rot", PosRot, cubePos)

	pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
	pub_takeoff = rospy.Publisher("/drone/takeoff", Empty, queue_size = 1)
	time.sleep(2)
	pub_takeoff.publish(empty)
	time.sleep(4)



	while(not rospy.is_shutdown()):
		if(((cube.position.x - drone.position.x) > 0.5) | ((cube.position.y - drone.position.y) > 0.5) | ((cube.position.z - drone.position.z) > 0.5)):
			vel.linear.x = 1*(cube.position.x - drone.position.x)
			print("Vel x: ",vel.linear.x)
			vel.linear.y = 1*(cube.position.y - drone.position.y)
			print("Vel y: ",vel.linear.y)
			vel.linear.z = 1*(cube.position.z - drone.position.z)
			print("Vel z: ",vel.linear.z)

		else:
			print("Zero Vel")
			vel.linear.x = 0
			vel.linear.y = 0
			vel.linear.z = 0
		pub_cmd_vel.publish(vel)

	rospy.spin()


if __name__ == '__main__':
    main()







