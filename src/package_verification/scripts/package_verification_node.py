#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

verification_publisher = None


def package_callback(msg):

    package_name = msg.data

    rospy.loginfo(f"[Scout] Received package: {package_name}")

    # Simulated verification logic
    if package_name == "Blue Box":
        result = f"Package Verified: {package_name}"
    else:
        result = f"Package Rejected: {package_name}"

    rospy.loginfo(f"[Scout] {result}")

    verification_publisher.publish(result)


def main():

    global verification_publisher

    rospy.init_node('package_verification_node')

    verification_publisher = rospy.Publisher(
        '/package_verified',
        String,
        queue_size=10
    )

    rospy.Subscriber(
        '/package_arrival',
        String,
        package_callback
    )

    rospy.loginfo("Package Verification Node Started")

    rospy.spin()


if __name__ == '__main__':
    main()