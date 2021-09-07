#!/usr/bin/env python3

import threading 
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
import av

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
from sensor_msgs.msg import Image, CompressedImage, Imu
from cv_bridge import CvBridge

def cb_ImageRaw(compMsg):

	img = np.array(compMsg.data)
	rawImage = br.cv2_to_imgmsg(img, 'bgr8')
	rawImage.header = compMsg.header
	pub_raw_Image.publish(rawImage)
	#print rawImage

def main():

	rospy.init_node('Tello_Raw_Video')
	
	global rawImage, pub_raw_Image, br
	rawImage = Image()
	br = CvBridge()

	sub_compImage = rospy.Subscriber('/tello/image_raw/h264', CompressedImage, cb_ImageRaw)
        
	pub_raw_Image= rospy.Publisher('tello/realRawImage', Image, queue_size=10)

	
	rospy.spin()
	return


if __name__ == '__main__':
    main()

