#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import time

arrival_publisher = None


def main():

    global arrival_publisher

    rospy.init_node('mover_controller')

    arrival_publisher = rospy.Publisher(
        '/package_arrival',
        String,
        queue_size=10
    )

    rospy.loginfo("[Mover] Starting warehouse mission")

    rospy.sleep(3)

    rospy.loginfo("[Mover] Delivering package to Scout")

    arrival_publisher.publish("Blue Box")

    rospy.loginfo("[Mover] Package delivered")

    rospy.spin()


if __name__ == '__main__':
    main()