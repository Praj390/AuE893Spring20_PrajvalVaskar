#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import math
import time
import numpy as np

def callback(points):
    leftdata = points.ranges[0:40]
    rightdata = points.ranges[314:359]
    usefuldata  = leftdata + rightdata
    if min(usefuldata)< 0.8:
        print('Stop')
        velocity.linear.x = 0
    else:
        print('moving')
        velocity.linear.x = 0.5
    return velocity


rospy.init_node('turtlebot3_world', anonymous=True)
velocity = Twist()
publish = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
subscribe = rospy.Subscriber('scan', LaserScan, callback)
rate = rospy.Rate(2)

while not rospy.is_shutdown():
    publish.publish(velocity)
    rate.sleep()
