#!/usr/bin/env python
import rospy
import math
from math import sqrt
import numpy as np
from geometry_msgs.msg import PoseArray,Twist
from nav_msgs.msg import Odometry
from people_msgs.msg import PositionMeasurementArray
import tf

kps_t = 0.4
kds_t = 0.0004
kis_t = 0.0015
uk1s_t = 0.0
er_1s_t = 0.0
er_2s_t = 0.0
tb_x_trans = 0.0
tb_y_trans = 0.0
tb_z_trans = 0.0
tb_x_or = 0.0
tb_y_or = 0.0 
tb_z_or = 0.0
tb_w_or = 0.0

def pose_callback(odom1_msg):
    global tb_x_trans,tb_y_trans,tb_z_trans,tb_x_or,tb_y_or,tb_z_or,tb_w_or
    tb_x_trans = odom1_msg.pose.pose.position.x
    tb_y_trans = odom1_msg.pose.pose.position.y
    tb_z_trans = odom1_msg.pose.pose.position.z
    tb_x_or = odom1_msg.pose.pose.orientation.x
    tb_y_or = odom1_msg.pose.pose.orientation.y
    tb_z_or = odom1_msg.pose.pose.orientation.z
    tb_w_or = odom1_msg.pose.pose.orientation.w


def callback(data):
    global kps_t, kds_t, kis_t, uk1s_t, er_1s_t, er_2s_t

    quaternion = (
    tb_x_or,
    tb_y_or,
    tb_z_or,
    tb_w_or)

    #convert the quaternion to roll-pitch-yaw
    rpy_tb = tf.transformations.euler_from_quaternion(quaternion)
    roll_tb = rpy_tb[0]
    pitch_tb = rpy_tb[1]
    yaw_tb = rpy_tb[2]

    vel_msg = Twist()
    velocity_publisher = rospy.Publisher('/cmd_vel',Twist,queue_size = 10)
    if len(data.people)!=0:
        
        man_x = data.people[0].pos.x
        man_y = data.people[0].pos.y
        man_z = data.people[0].pos.z 

        distance = sqrt((tb_x_trans - man_x)**2 + (tb_y_trans-man_y)**2)
        error_x = distance - 0.5
        distance_angular = (math.atan2(man_y-tb_y_trans,man_x-tb_x_trans))-yaw_tb
        error_z = distance_angular


        k_1s_t = kps_t + kis_t + kds_t
        k_2s_t = -kps_t - (2.0 * kds_t)
        k_3s_t = kds_t

        uks_t = uk1s_t + (k_1s_t * error_x) + (k_2s_t * er_1s_t) + (k_3s_t * er_2s_t)
        uks_t = uks_t
        uk1s_t = uks_t
        er_2s_t = er_1s_t
        er_1s_t = error_x

        if error_x>0.005:
            vel_msg.linear.x = uks_t*0.7
            # print("positive x vel",vel_msg.linear.x)
        elif error_x<=0.002:
            vel_msg.linear.x = uks_t*0.4
            # print("negative x vel",vel_msg.linear.x)
        elif 0.002<error_x<=0.005:
            vel_msg.linear.x = 0.0
            print("xstop")
        if error_z>-0.7:
            vel_msg.angular.z = error_z*0.6
            # print("z_vel", vel_msg.angular.z)
        else:
            vel_msg.angular.z = 0
            print("zstop")
    else:
        print("Too far, moving closer")
        vel_msg.linear.x = 0.005
        vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

def main():
    rospy.init_node('follow_man',anonymous=True)
    rospy.Subscriber('/odom',Odometry,pose_callback)
    rospy.Subscriber('/people_tracker_measurements',PositionMeasurementArray,callback)
    
while not rospy.is_shutdown():
    main()
    rate = rospy.Rate(1)
    rate.sleep()