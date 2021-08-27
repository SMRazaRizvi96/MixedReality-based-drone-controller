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
from drone_control.msg import TargetPose
from drone_control.msg import QRPose


def recv():
    count = 0
    global feedback
    while True: 
        try:
            data, server = sock.recvfrom(1518)
	    feedback = data.decode(encoding="utf-8")
            #print(data.decode(encoding="utf-8"))
	    print (feedback)
        except Exception:
            print ('\nExit . . .\n')
            break


def cubePos(currentcubePos):
    global cube
    cube.position.x = -currentcubePos.pos_z
    cube.position.y = currentcubePos.pos_x
    cube.position.z = currentcubePos.pos_y

def telloPos(currenttelloPos):
    global tello
    #tello.position.x = -currenttelloPos.QR_pos_z
    #tello.position.y = currenttelloPos.QR_pos_x
    #tello.position.z = currenttelloPos.QR_pos_y
    tello.position.x = -currenttelloPos.QR_pos_z
    tello.position.y = currenttelloPos.QR_pos_x + 0.1
    tello.position.z = currenttelloPos.QR_pos_y + 0.05

def userInput():
	global feedback
	feedback = ''

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
		#while('ok' not in feedback):
			

	    except KeyboardInterrupt:
		print ('\n . . .\n')
		#sock.close()  
		break
	return msg

def trackCube():
# Sending go to commands to the Tello
	global feedback
	telloPose = Pose()
	cubePose = Pose()
	feedback = ''
	g = 0

	while(not rospy.is_shutdown()):
	    try:
		cubePose = cube
		telloPose = tello
		#print("Cube x: ", cubePose.position.x, " Cube y: ", cubePose.position.y, " Cube z: ", cubePose.position.z)
		#print("Tello x: ", telloPose.position.x, " Tello y: ", telloPose.position.y, " Tello z: ", telloPose.position.z)
		goalPose.position.x = 100*(cubePose.position.x - telloPose.position.x)
		goalPose.position.y = 100*(cubePose.position.y - telloPose.position.y)
		goalPose.position.z = 100*(cubePose.position.z - telloPose.position.z)
		#print("Goal x: ", goalPose.position.x, " Goal y: ", goalPose.position.y, " Goal z: ", goalPose.position.z)

		
		if(telloPose):

			if (abs(goalPose.position.x) > 20 or abs(goalPose.position.y) > 20 or abs(goalPose.position.z) > 20):
				g+=1
				print ('Goal Command: ', g)

			# For Forward and Backward

			if (abs(goalPose.position.x) > 20):

				if (goalPose.position.x < 0):

					msg = "back " + str(abs(goalPose.position.x))

				else:
					msg = "forward " + str(abs(goalPose.position.x))

			else:
				msg = "stop"

			#print("I updated msg")


			msg = msg.encode(encoding="utf-8")
			feedback = ''

			i = 1
			
			counter = time.clock()

			#while (('ok' not in feedback or 'error' in feedback) and ('out of range' not in feedback and i < 4)):

			while (('error' in feedback) or (feedback == '') and (i < 4) and (abs(100*(cube.position.x - tello.position.x)) > 20) and ('stop' not in msg)):

			# What happens if the difference is still greater than 20, but not exactly what you computed before? So maybe the difference in coordinate should be calculated again? Or no?

				sent = sock.sendto(msg, tello_address)
				#print("Msg sent: ", msg)

				#print 'Waiting for feedback'

				t = time.clock()
				elapsed = 0
				i+=1
				
				while(feedback=='' and not rospy.is_shutdown() and elapsed < 4):
					if ('error' in feedback):
						break
					if ('out of range' in feedback):
						break
					elapsed = time.clock() - t

			if ('stop' not in msg):
				if ('ok' in feedback):
					print('X Coordinate reached in ', time.clock() - counter, ' seconds')
					print('Goal x: ', goalPose.position.x)
					print('Cube x: ', 100*cube.position.x)
					print('Tello x: ', 100*tello.position.x)
					print('Difference in x Coordinate: ', 100*cube.position.x-100*tello.position.x, ' cm')

				else:
					print ('X Coordinate not reached properly because feedback = ', feedback)

			# Now for Left - Right

			if (abs(goalPose.position.y) > 20):

				if (goalPose.position.y < 0):

					msg = "right " + str(abs(goalPose.position.y))

				else:
					msg = "left " + str(abs(goalPose.position.y))

			else:
				msg = "stop"

			#print("I updated msg")


			msg = msg.encode(encoding="utf-8")
			feedback = ''

			i = 1

			counter = time.clock()

			while (('error' in feedback) or (feedback == '') and (i < 4) and  (abs(100*(cube.position.y - tello.position.y)) > 20) and ('stop' not in msg)):

				sent = sock.sendto(msg, tello_address)
				#print("Msg sent: ", msg)

				#print 'Waiting for feedback'

				t = time.clock()
				elapsed = 0
				i+=1
				
				while(feedback=='' and not rospy.is_shutdown() and elapsed < 5):
					if ('error' in feedback):
						break
					if ('out of range' in feedback):
						break
					elapsed = time.clock() - t

			if ('stop' not in msg):

				if ('ok' in feedback):
					print('Y Coordinate reached in ', time.clock() - counter, ' seconds')
					print('Goal y: ', goalPose.position.y)
					print('Cube y: ', 100*cube.position.y)
					print('Tello y: ', 100*tello.position.y)
					print('Difference in y Coordinate: ', 100*cube.position.y-100*tello.position.y, ' cm')

				else:
					print ('Y Coordinate not reached properly because feedback = ', feedback)

			# Now for Up - Down

			if (abs(goalPose.position.z) > 20):

				if (goalPose.position.z < 0):

					msg = "down " + str(abs(goalPose.position.z))

				else:
					msg = "up " + str(abs(goalPose.position.z))

			else:
				msg = "stop"

			#print("I updated msg")


			msg = msg.encode(encoding="utf-8")
			feedback = ''

			i = 1

			counter = time.clock()

			while (('error' in feedback) or (feedback == '') and (i < 4) and (abs(100*(cube.position.z - tello.position.z)) > 20) and ('stop' not in msg)):

				sent = sock.sendto(msg, tello_address)
				#print("Msg sent: ", msg)

				#print 'Waiting for feedback'
				
				t = time.clock()
				elapsed = 0
				i+=1

				while(feedback=='' and not rospy.is_shutdown() and elapsed < 5):
					if ('error' in feedback):
						break
					if ('out of range' in feedback):
						break
					elapsed = time.clock() - t


			if ('stop' not in msg):
				if ('ok' in feedback):
					print('Z Coordinate reached in ', time.clock() - counter, ' seconds')
					print('Goal z: ', goalPose.position.z)
					print('Cube z: ', 100*cube.position.z)
					print('Tello z: ', 100*tello.position.z)
					print('Difference in z Coordinate: ', 100*cube.position.z-100*tello.position.z, ' cm')

				else:
					print ('Z Coordinate not reached properly because feedback = ', feedback)

		
	    except KeyboardInterrupt:
		print ('\n . . .\n')
		#sock.close() 
		check = False 
		break


def main():

	rospy.init_node('Tello_Server')

	global cube, tello, sock, tello_address, goalPose, feedback
	cube = Pose()
	tello = Pose()
	goalPose = Pose()
	
	sub_cube = rospy.Subscriber("/target_pose", TargetPose, cubePos)
	sub_tello = rospy.Subscriber("/qr_code_pose", QRPose, telloPos)

	host = ''
	port = 9000
	locaddr = (host,port) 


	# Create a UDP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	#tello_address = ('192.168.10.1', 8889)
	tello_address = ('172.20.10.5', 8889) 
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



