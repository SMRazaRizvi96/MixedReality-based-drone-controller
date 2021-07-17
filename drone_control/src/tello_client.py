#!/usr/bin/env python

# Tello Python3 Control Demo 
#
# http://www.ryzerobotics.com/
#
# 1/1/2018

# This is a Client replicating the behavior of the Tello drone.
# This client receives the UDP Packets from a Server.
# These packets contains commands to execute.

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
from unity_robotics_demo_msgs.msg import PosRot


def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


def main():

	rospy.init_node('Tello_Client')

	# Create a UDP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	tello_address = ('172.20.135.150', 8889) 
	sock.bind(tello_address)

	while True: 
		try:
		    data, server = sock.recvfrom(1518)
		    print(data.decode(encoding="utf-8"))
		except Exception:
		    print ('\nExit . . .\n')
		    break

	rospy.spin()


if __name__ == '__main__':
    main()


