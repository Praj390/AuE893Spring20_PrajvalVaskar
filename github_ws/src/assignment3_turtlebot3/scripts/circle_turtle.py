#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def move_circle():
    # Starts a new node
    rospy.init_node('circle_turtlebot', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


    #Create twist msgs
    move_cmd = Twist()
    move_cmd.linear.x = 0.5
    move_cmd.angular.z = 0.5


    # Save current time and set publish rate
    now = rospy.Time.now()
    rate = rospy.Rate(10)


    while rospy.Time.now() < now + rospy.Duration.from_sec(20):
	velocity_publisher.publish(move_cmd)
	rate.sleep()




if __name__ == '__main__':
    try:
        #Testing our function
        move_circle()
    except rospy.ROSInterruptException:
        pass
