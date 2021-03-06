#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from darknet_ros_msgs.msg import BoundingBoxes
from move_robot import MoveTurtlebot3

ctr = 0

class LineFollower(object):

    def __init__(self):
    
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.detection_sub = rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, self.detection_callback)
        self.moveTurtlebot3_object = MoveTurtlebot3()

    def camera_callback(self,data):
        
        try:
            # We select bgr8 because its the OpneCV encoding by default
	        cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
            
        # We get image dimensions and crop the parts of the image we dont need
        height, width, channels = cv_image.shape
        crop_img = cv_image[(height/2)+220:height][1:width]
        
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
        m = cv2.moments(mask, False)

        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
            cx, cy = height/2, width/2

        res = cv2.bitwise_and(crop_img,crop_img, mask= mask)
        # Draw the centroid in the resultut image
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) 
        cv2.circle(res,(int(cx), int(cy)), 10,(0,0,255),-1)

        # cv2.imshow("Original", cv_image)
        #cv2.imshow("MASK", mask)
        cv2.imshow("RES", res)
        cv2.waitKey(1)

        """
	    Enter controller here.
        """
        error_x = cx - (height / 2) - 89
        twist_object = Twist()
        twist_object.linear.x = 0.005
        twist_object.angular.z = -error_x / 2250
        rospy.loginfo("ANGULAR VALUE SENT===>"+str(twist_object.angular.z))
        # Make it start turning
        self.moveTurtlebot3_object.move_robot(twist_object)

    def detection_callback(self, msg):
        global ctr
        for x in range(len(msg.bounding_boxes)):
            twist_object = Twist()
            if msg.bounding_boxes[x].Class == "stop sign" and ctr == 0:
                twist_object.linear.x = 0
                twist_object.angular.z = 0
                self.moveTurtlebot3_object.move_robot(twist_object)
                rospy.sleep(3)
                ctr = 1

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
