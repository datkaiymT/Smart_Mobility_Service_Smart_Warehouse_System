#!/usr/bin/env python3
import rospy
from cli_manager.msg import RobotStatus

def talker():
    pub = rospy.Publisher('robot_status', RobotStatus, queue_size=10)
    rospy.init_node('robot_publisher', anonymous=True)
    rate = rospy.Rate(1) # 1hz
    
    while not rospy.is_shutdown():
        # Create an instance of your custom message
        status = RobotStatus()
        status.robot_id = "Robot_Alpha"
        status.battery_level = 85.5
        status.current_task = "Moving to Dock"
        
        rospy.loginfo(f"Publishing: {status.robot_id}")
        pub.publish(status)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass