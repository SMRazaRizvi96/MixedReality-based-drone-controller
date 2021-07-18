#!/usr/bin/env python

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
import tellopy

# Ros Messages

from geometry_msgs.msg import Twist, Point, Pose
from std_msgs.msg import Empty
from std_msgs.msg import String
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from unity_robotics_demo_msgs.msg import PosRot

def flight_data_callback(self, event, sender, data, **args):
	flight_data = FlightData()

	# Battery state
	flight_data.battery_percent = data.battery_percentage
	flight_data.estimated_flight_time_remaining = data.drone_fly_time_left / 10.
        rospy.loginfo('Drone Battery: ', flight_data.battery_percent)

	# Flight mode
	flight_data.flight_mode = data.fly_mode

	# Flight time
	flight_data.flight_time = data.fly_time

def main():

	rospy.init_node('Tello_Server_Library')

	tello = tellopy.Tello()

	tello.connect()
	tello.wait_for_connection(60.0)
        rospy.loginfo('connected to drone')

        #rospy.subscribe(tello.EVENT_FLIGHT_DATA, flight_data_callback)
	#tello.takeoff()

	#tello.move_left(100)
	#tello.rotate_clockwise(90)
	#tello.move_forward(100)

	#tello.land()

	tello.quit()
        tello = None

	rospy.spin()



if __name__ == '__main__':
    main()

