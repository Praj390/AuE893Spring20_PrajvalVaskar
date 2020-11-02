#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from move_robot import MoveTurtlebot3
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from apriltag_ros.msg import AprilTagDetectionArray
from std_msgs.msg import String
import math
import time

kps = 1.1
kds = 0.00065
kis = 0.05
uk1s = 0.0
er_1s = 0.0
er_2s = 0.0
rospy.loginfo("START BEGINNING")
class Integrator(object):
    def __init__(self):
        rospy.loginfo("START")
        # rospy.on_shutdown(self.shutdown)
        self.velocity = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.laser_distance = rospy.Subscriber('scan', LaserScan, self.laser_distance_callback, queue_size=10)
        # self.apriltag_image_sub = rospy.Subscriber('/tag_detections_image', Image, self.apriltag_image_callback,queue_size=10)
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.image_callback,queue_size=10)
        self.sub = rospy.Subscriber('/tag_detections', AprilTagDetectionArray, self.apriltag_callback,queue_size=10)
        self.distance = LaserScan()
        # self.tag_image = Image()
        self.tag = AprilTagDetectionArray()
        self.image = Image()
        self.bridge_object = CvBridge()
        self.errors = 0
        self.error_x = 0
        self.forward1 = 0
        self.forward2 = 0

    def laser_distance_callback(self, data1):
        self.laser_distance = data1
        self.distance_error()
        rospy.loginfo("DISTANCE")

    def distance_error(self):
        frontleft = self.laser_distance.ranges[20:80]
        frontright = self.laser_distance.ranges[300:339]
        left = []
        right = []
        for i in frontleft:
            if 0 < i < 10:
                left.append(i)
        for j in frontright:
            if 0 < j < 10:
                right.append(j)
        self.errors = np.mean(right) - np.mean(left)

    # def apriltag_image_callback(self, data2):
    #     self.tag_image = data2
    #     cv_image = self.bridge_object.imgmsg_to_cv2(data2, desired_encoding="bgr8")
    #     cv2.imshow("Scan", cv_image)
    #     cv2.waitKey(2)
    #     rospy.loginfo("APRIL TAG IMAGE")

    def image_callback(self, data3):
        # self.image = data3
        try:
	        cv_image = self.bridge_object.imgmsg_to_cv2(data3, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
            
        height, width, channels = cv_image.shape
        crop_img = cv_image[(height/2)+220:height][1:width]
        
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        
        lower_yellow = np.array([20,100,100])
        upper_yellow = np.array([50,255,255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        m = cv2.moments(mask, False)

        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
            cx, cy = height/2, width/2

        res = cv2.bitwise_and(crop_img,crop_img, mask= mask)
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) 
        cv2.circle(res,(int(cx), int(cy)), 2,(0,0,255),-1)
        # cv2.imshow("Original", cv_image)
        #cv2.imshow("MASK", mask)
        cv2.imshow("RES", res)
        cv2.waitKey(2)

        self.error_x = cx - (height / 2) - 89

        rospy.loginfo("LINE FOLLOWING IMAGE")
        
    def apriltag_callback(self, data4):
        rospy.loginfo("APRIL TAG")
        self.tag = data4
        try:
            self.forward1 = data4.detections[0].pose.pose.pose.position.z
            self.forward2 = data4.detections[1].pose.pose.pose.position.z
        except IndexError:
            rospy.loginfo('No tag detected')

    def MoveController(self):
        rospy.loginfo("IN THE CONTROLLER")
        global kps, kds, kis, uk1s, er_1s, er_2s
        vel = Twist()

        rate = rospy.Rate(20)

        # while not rospy.is_shutdown():
        k_1s = kps + kis + kds
        k_2s = -kps - (2.0 * kds)
        k_3s = kds

        uks = uk1s + (k_1s * self.errors) + (k_2s * er_1s) + (k_3s * er_2s)
        uks = uks
        uk1s = uks
        er_2s = er_1s
        er_1s = self.errors

        vel.linear.x = 0.1

        if self.errors == 0:
            vel.angular.z = 0.0
        else:
            vel.angular.z = -uks
        self.velocity.publish(vel)
        rospy.loginfo(vel)
        rospy.loginfo("SETTING VELOCITY IN THE CONTROLLER")
        
        rate.sleep()
        self.velocity.publish(vel)

    # def shutdown(self):
    #     rospy.loginfo("ESSSSTTTTTAAAAAPPPPPPP")
    #     self.velocity.publish(Twist())
    #     time.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node('AuEFinal', anonymous=False)
        chodu = Integrator()

        # while not rospy.is_shutdown():
        rospy.loginfo("TRYING EXECUTING CONTROLLER")
        chodu.MoveController()
        rospy.loginfo("EXECUTED CONTROLLER")

    except rospy.ROSInterruptException:
        rospy.loginfo("ROS INTERRUPTED")




