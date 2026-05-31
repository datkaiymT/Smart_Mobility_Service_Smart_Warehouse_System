#!/usr/bin/env python3
import rospy

if __name__ == '__main__':
    rospy.init_node('hello_node')
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        rospy.loginfo("Project started successfully!")
        rate.sleep()
