#!/usr/bin/env python
import rospy
import math
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

def callback(msg):
    left_data = msg.ranges[20:90]
    right_data = msg.ranges[270:339]
    front_data_l =  msg.ranges[0:20]
    front_data_r = msg.ranges[339:359]
    front_data = front_data_l + front_data_r
    # front_data = np.asarray(front_data)
    # right_data = np.asarray(right_data)
    # left_data = np.asarray(left_data)
    # front_data[front_data >= 99999999] = 7
    # right_data[right_data >= 99999999] = 7
    # left_data[left_data >= 99999999] = 7
    right_distance = np.min(right_data)
    left_distance = np.min(left_data)
    front_distance = np.min(front_data)

    if front_distance < 0.5:
        if left_distance > front_distance :
            vel_msg.linear.x = 0
            vel_msg.angular.z = 1
            print("left")
            # print((np.mean(left_data)))
            # print("lol")
            # print((np.mean(front_data)))
        elif right_distance > front_distance:
            vel_msg.linear.x = 0
            vel_msg.angular.z = -1
            print("right")
            # print((np.mean(right_data)))
            # print("bol")
        else:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 1
            print("rotate")
    else:
        vel_msg.linear.x = 0.3
        vel_msg.angular.z = 0

    return vel_msg

rospy.init_node('wander_tutrle', anonymous=True)
vel_msg = Twist()
velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size = 20)
sub = rospy.Subscriber('scan', LaserScan, callback)
rate = rospy.Rate(2)


while not rospy.is_shutdown():
    velocity_publisher.publish(vel_msg)
    rate.sleep()
