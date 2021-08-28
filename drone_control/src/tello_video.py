#!/usr/bin/env python

# Tello Python3 Control Demo 
#
# http://www.ryzerobotics.com/
#
# 1/1/2018

# This is a Server. TELLO has its own client.
# Type the commands, and it will send the UDP Packets to the UDP CLients.
# Problem to solve: Once ctrl-c from Track, you cannot type track again and go to Tracking

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
import cv2

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
from unity_robotics_demo_msgs.msg import QRPose

def recv_video():
    count = 0
    while True: 
        try:
	    print 'rec'
            data, server = sock_video.recvfrom(1518)
	    feedback_video = data.decode(encoding="utf-8")
            #print(data.decode(encoding="utf-8"))
	    print (feedback_video)
        except Exception:
            print ('\nExit . . .\n')
            break


def main():

	rospy.init_node('Tello_Video_Server')

	global feedback_video,sock_video
	feedback_video = 'Nothing'

	host = ''
	video_port = 11111
	locaddr_video = (host,video_port) 
        address_schema = 'udp://@{ip}:{port}'  # + '?overrun_nonfatal=1&fifo_size=5000'
        address = address_schema.format(host, video_port)


	# Create a UDP socket
	sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_video.bind(locaddr_video)
	


	print ('\r\n\r\nTello Python3 Demo.\r\n')

	print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

	print ('end -- quit demo.\r\n')

	#recvThread create
	recvThread_video = threading.Thread(target=recv_video)
	recvThread_video.start()

	while(not rospy.is_shutdown()):
		#print feedback_video
            cap = cv2.VideoCapture(address)

	sock_video.close()
	
	rospy.spin()
	return


if __name__ == '__main__':
    main()

