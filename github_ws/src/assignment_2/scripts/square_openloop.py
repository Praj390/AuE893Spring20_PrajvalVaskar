#!/usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist


def move_straight():
    speed = 0.2
    distance = 2

    vel_msg.linear.x = 0.2
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    t0 = rospy.Time.now().to_sec()
    current_distance = 0
    while(current_distance < distance):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_distance = speed*(t1 - t0)

    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)

def rotate():
    angular_speed = 0.2
    desired_angle = 90*math.pi/180

    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = angular_speed

    t0 = rospy.Time.now().to_sec()
    current_angle = 0
    while(current_angle < desired_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1 - t0)

    vel_msg.linear.z = 0
    velocity_publisher.publish(vel_msg)


if __name__ == '__main__':
    try:
        #Testing our function
        rospy.init_node('square_openloop')
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
        vel_msg = Twist()
        for n in range(4):
            move_straight()
            rotate()
    except rospy.ROSInterruptException:
        pass
