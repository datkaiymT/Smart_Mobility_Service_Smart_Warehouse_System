#!/usr/bin/env python3

import rospy
from std_msgs.msg import String


def verification_callback(msg):

    rospy.loginfo(f"[Coordinator] {msg.data}")

    rospy.loginfo("[Coordinator] Mission completed successfully")


def main():

    rospy.init_node('coordinator_node')

    rospy.Subscriber(
        '/package_verified',
        String,
        verification_callback
    )

    rospy.loginfo("Coordinator Node Started")

    rospy.spin()


if __name__ == '__main__':
    main()