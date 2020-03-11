#!/usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

def callback(msg):
    l_data = msg.ranges[0:39]
    r_data = msg.ranges[320:359]
    data = l_data+r_data
    if min(data) < 0.8:
        print('Stop')
        # vel_msg.linear.x = 0.1
        vel_msg.linear.x = 0
    else:
        print('moving')
        vel_msg.linear.x = 0.2
    return vel_msg


rospy.init_node('move_straight', anonymous=True)
vel_msg = Twist()
velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
sub = rospy.Subscriber('scan', LaserScan, callback)
rate = rospy.Rate(2)


while not rospy.is_shutdown():
    velocity_publisher.publish(vel_msg)
    rate.sleep()
