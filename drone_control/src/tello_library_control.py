#!/usr/bin/env python3
import rospy
import sys
import traceback
import tellopy
import av
#import cv2.cv2 as cv2  # for avoidance of pylint error
import cv2
import numpy
import time

from geometry_msgs.msg import Twist

def cb_cmd_vel(msg):
	drone.set_pitch( drone.__scale_vel_cmd(msg.linear.y) )
	drone.set_roll( drone.__scale_vel_cmd(msg.linear.x) )
	drone.set_yaw( drone.__scale_vel_cmd(msg.angular.z) )
	drone.set_throttle(drone.__scale_vel_cmd(msg.linear.z) )



def main():

	global drone
	drone = tellopy.Tello()
    
	pub_odom = rospy.Publisher('cmd_vel', Twist, queue_size=1, latch=True)
	sub_cmd_vel = rospy.Subscriber('cmd_vel', Twist, cb_cmd_vel)

	try:
		drone.connect()
		drone.wait_for_connection(60.0)      

	except Exception as ex:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		print(ex)
		
	while(1):
		print('Working')
	drone.quit()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
