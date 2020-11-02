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
from darknet_ros_msgs.msg import BoundingBoxes
from std_msgs.msg import String
import math
import time

right = 0.0
left = 0.0
uk1s = 0.0
er_1s = 0.0
er_2s = 0.0
errors = 0.0
line_following_mode = False
finding_lane = True
stop_sign_found = False
count = 0.0

class LineFollower(object):

    def __init__(self):
    
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.moveTurtlebot3_object = MoveTurtlebot3()

    def camera_callback(self,data):
        
        try:
            # We select bgr8 because its the OpneCV encoding by default
	        cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
            
        # We get image dimensions and crop the parts of the image we dont need
        height, width, channels = cv_image.shape
        crop_img = cv_image[(height)/2+120:height][1:width]
        
        # Convert from RGB to HSV
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        
        # Define the Yellow Colour in HSV

        """
        To know which color to track in HSV use ColorZilla to get the color registered by the camera in BGR and convert to HSV. 
        """

        # Threshold the HSV image to get only yellow colors
        lower_yellow = np.array([20,100,100])
        upper_yellow = np.array([50,255,255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Calculate centroid of the blob of binary image using ImageMoments
       
        global line_following_mode

        m = cv2.moments(mask, False)

        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
            line_following_mode = True
            finding_lane = False
        except ZeroDivisionError:
            cx, cy = height/2, width/2
            finding_lane = True
            line_following_mode = False

        res = cv2.bitwise_and(crop_img,crop_img, mask= mask)

        cv2.circle(res,(int(cx), int(cy)), 10,(0,0,255),-1)

        # cv2.imshow("Original", cv_image)
        #cv2.imshow("MASK", mask)
        cv2.imshow("RES", res)
        cv2.waitKey(1)

        twist_object = Twist()

        global errors, uks, uk1s, er_1s, er_2s

        if finding_lane:
            rospy.loginfo("FINDING LINE")
            def wall_following_callback(points):
                global right, left
                frontleft = points.ranges[20:80]
                frontright = points.ranges[300:339]
                left = []
                right = []
                for i in frontleft:
                    if 0 < i < 10:
                        left.append(i)
                for j in frontright:
                    if 0 < j < 10:
                        right.append(j)
                right = np.mean(right)
                left = np.mean(left)
                return left, right

            wall_following_sub = rospy.Subscriber('scan', LaserScan, wall_following_callback)

            kps = 1.1
            kds = 0.00065
            kis = 0.05

            errors = right - left
            k_1s = kps + kis + kds
            k_2s = -kps - (2.0 * kds)
            k_3s = kds

            uks = uk1s + (k_1s * errors) + (k_2s * er_1s) + (k_3s * er_2s)
            uks = uks
            uk1s = uks
            er_2s = er_1s
            er_1s = errors

            twist_object.linear.x = 0.1
            if errors == 0:
                twist_object.angular.z = 0.0
            else:
                twist_object.angular.z = -uks

            
        if line_following_mode:

            def detection_callback(msg):
                global count
                global stop_sign_found
                for x in range(len(msg.bounding_boxes)):
                    if msg.bounding_boxes[x].Class == "stop sign":
                        stop_sign_found = True
                        count += 1
                            
            stop_sign_sub = rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, detection_callback)
            print("COUNTER IS AT",count)
            if stop_sign_found and 0 < count < 133:
                ("STOP SIGN MODE")
                t = rospy.get_time()
                T = t
                while T <= t + 3.0:
                    twist_object.linear.x = 0
                    twist_object.angular.z = 0
                    # self.moveTurtlebot3_object.move_robot(twist_object)
                    T = rospy.get_time()
            else:
                rospy.loginfo("LINE FOLLOWING MODE AFTER STOPPING")
                error_x = cx - (height / 2) - 89
                twist_object.linear.x = 0.1
                twist_object.angular.z = -error_x / 850

            # rospy.loginfo("LINE FOLLOWING MODE")
            # error_x = cx - (height / 2) - 89
            # twist_object.linear.x = 0.1
            # twist_object.angular.z = -error_x / 850


        self.moveTurtlebot3_object.move_robot(twist_object)
        
    def clean_up(self):
        self.moveTurtlebot3_object.clean_class()
        cv2.destroyAllWindows()     

def main():
    rospy.init_node('line_following_node', anonymous=True)
    
    
    line_follower_object = LineFollower()

    
    rate = rospy.Rate(5)
    ctrl_c = False
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        line_follower_object.clean_up()
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        rate.sleep()

    
    
if __name__ == '__main__':
    main()