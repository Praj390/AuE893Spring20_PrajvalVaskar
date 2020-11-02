#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from apriltag_ros.msg import AprilTagDetectionArray
from move_robot import MoveTurtlebot3

forward1 = 0
forward2 = 0


class Apriltag_follower(object):

    def __init__(self):

        self.bridge_object = CvBridge()
        self.publish = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.image_sub = rospy.Subscriber('/tag_detections_image', Image, self.camera_callback)
        self.sub = rospy.Subscriber('/tag_detections', AprilTagDetectionArray, self.callback)

    def camera_callback(self, data):

        cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        cv2.imshow("Scan", cv_image)
        cv2.waitKey(1)

    def callback(self, data):
        global forward1, forward2
        try:
            forward1 = data.detections[0].pose.pose.pose.position.z
            forward2 = data.detections[1].pose.pose.pose.position.z
        except IndexError:
            rospy.loginfo('No tag detected')


def main():
    rospy.init_node('april_tag_node', anonymous=True)

    Apriltag_follower()

    rate = rospy.Rate(5)

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    main()
