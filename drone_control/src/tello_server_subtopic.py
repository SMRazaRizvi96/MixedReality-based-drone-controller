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


def cubePos(currentcubePos):
    
    cube.position.x = 10*currentcubePos.pos_x
    cube.position.y = 10*currentcubePos.pos_y
    cube.position.z = 10*currentcubePos.pos_z
    #print("Cube x: ", cube.position.x, "Drone y: ", cube.position.y, "Drone z: ", cube.position.z)

def userInput():

	while True: 
	    try:
		python_version = str(platform.python_version())
		version_init_num = int(python_version.partition('.')[0]) 
	        print ('Type the commands to send to Tello\n')
		if version_init_num == 3:
		    msg = input("");
		elif version_init_num == 2:
		    msg = raw_input("");
		
		if not msg:
		    break  

		if 'track' in msg:
		    print ('...')
		    #sock.close() 
		    break

		if 'stop' in msg:
		    print ('...')
		    #sock.close() 
		    break

		# Send data
		msg = msg.encode(encoding="utf-8") 
		sent = sock.sendto(msg, tello_address)
		print("Msg sent: ", msg)

	    except KeyboardInterrupt:
		print ('\n . . .\n')
		#sock.close()  
		break
	return msg

def trackCube():
# Sending go to commands to the Tello

	while(not rospy.is_shutdown()):
	    try:
		msg = "go " + str(cube.position.x) + " " + str(cube.position.y) + " " + str(cube.position.z) + " " + str(1)
		# Send data
		msg = msg.encode(encoding="utf-8")
		time.sleep(0.5)
		sent = sock.sendto(msg, tello_address)
		print("Msg sent: ", msg)

	    except KeyboardInterrupt:
		print ('\n . . .\n')
		#sock.close() 
		check = False 
		break


def main():

	rospy.init_node('Tello_Server')

	global cube, sock, tello_address
	cube = Pose()
	#cube.position.x = 1
	#cube.position.y = 2
	#cube.position.z = 3

	sub_cube = rospy.Subscriber("/pos_rot", PosRot, cubePos)

	host = ''
	port = 9000
	locaddr = (host,port) 


	# Create a UDP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	#tello_address = ('192.168.10.1', 8889)
	tello_address = ('172.20.135.150', 8889) 
	sock.bind(locaddr)


	print ('\r\n\r\nTello Python3 Demo.\r\n')

	print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

	print ('end -- quit demo.\r\n')


	#recvThread create
	recvThread = threading.Thread(target=recv)
	recvThread.start()

	msg = ""

	while(not 'stop' in msg):
		msg = userInput()

		if('track' in msg):
			trackCube()
	
	msg = "go 0 0 0 1"
	# Send data
	msg = msg.encode(encoding="utf-8") 
	sent = sock.sendto(msg, tello_address)
	print("Msg sent: ", msg)

	#msg = "land"
	# Send data
	#msg = msg.encode(encoding="utf-8") 
	#sent = sock.sendto(msg, tello_address)
	#print("Msg sent: ", msg)

	python_version = str(platform.python_version())
	version_init_num = int(python_version.partition('.')[0]) 
        print ('Type land to land and turn-off the Tello\n')

	if version_init_num == 3:
	    msg = input("");
	elif version_init_num == 2:
	    msg = raw_input("");

	# Send data
	msg = msg.encode(encoding="utf-8") 
	sent = sock.sendto(msg, tello_address)
	print("Msg sent: ", msg)
	sock.close()
	
	rospy.spin()


if __name__ == '__main__':
    main()

