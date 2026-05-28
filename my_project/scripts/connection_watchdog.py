#!/usr/bin/env python3
import rospy
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry  # <--- Added to read robot position data

class ResilientWatchdog:
    def __init__(self):
        rospy.init_node('resilient_watchdog', anonymous=True)
        
        self.last_heartbeat_time = rospy.get_time()
        self.timeout_duration = 2.0  
        self.connection_lost = False

        # History list to save coordinates [(x1, y1), (x2, y2), ...]
        self.path_history = []
        self.max_history_length = 500  # Save last 500 spots

        # Current position variables
        self.current_x = 0.0
        self.current_y = 0.0

        # Subscribers
        rospy.Subscriber('/ui_heartbeat', String, self.heartbeat_callback)
        rospy.Subscriber('/odom', Odometry, self.odom_callback) # Tracks where robot is
        
        # Publishers
        self.status_pub = rospy.Publisher('/comm_status', Bool, queue_size=10)
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        rospy.loginfo("Resilient Watchdog Active. Recording trail...")

    def odom_callback(self, data):
        # Update current coordinates from robot sensors
        self.current_x = data.pose.pose.position.x
        self.current_y = data.pose.pose.position.y
        
        # Only record history if the connection is perfectly healthy
        if not self.connection_lost:
            self.path_history.append((self.current_x, self.current_y))
            # Keep history from growing forever (removes oldest points)
            if len(self.path_history) > self.max_history_length:
                self.path_history.pop(0)

    def heartbeat_callback(self, msg):
        self.last_heartbeat_time = rospy.get_time()
        if self.connection_lost:
            rospy.logwarn("Connection RESTORED! Resuming normal mission.")
            self.connection_lost = False

    def monitor_loop(self):
        rate = rospy.Rate(10) 
        while not rospy.is_shutdown():
            current_time = rospy.get_time()
            time_since_last_heartbeat = current_time - self.last_heartbeat_time
            
            if time_since_last_heartbeat > self.timeout_duration:
                if not self.connection_lost:
                    rospy.logerr("CRITICAL: Signal lost! Reversing along path history...")
                    self.connection_lost = True
                
                self.status_pub.publish(False)
                self.execute_return_home()
            else:
                self.status_pub.publish(True)
                
            rate.sleep()

    def execute_return_home(self):
        cmd = Twist()
        # If we have points in our history, go back to the last known safe spot
        if len(self.path_history) > 0:
            target_x, target_y = self.path_history[-1] # Get last safe spot
            
            # Simple logic: If we are close enough to that point, remove it and target the one before it
            distance = ((target_x - self.current_x)**2 + (target_y - self.current_y)**2)**0.5
            if distance < 0.2: 
                self.path_history.pop() # Arrived at this breadcrumb, throw it away
                rospy.loginfo("Reached breadcrumb. Retracting further...")
            
            # Drive backwards safely
            cmd.linear.x = -0.2  # Move backward slowly
            cmd.angular.z = 0.0  # Keep wheels straight for now
        else:
            # If history is empty, we are back at the start! Stop and wait.
            rospy.logwarn("Back at initial starting point. Full stop.")
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            
        self.vel_pub.publish(cmd)

if __name__ == '__main__':
    try:
        watchdog = ResilientWatchdog()
        watchdog.monitor_loop()
    except rospy.ROSInterruptException:
        pass
