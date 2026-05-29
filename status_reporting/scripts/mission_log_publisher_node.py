#!/usr/bin/env python3
# =============================================================================
# mission_log_publisher_node.py
# -----------------------------------------------------------------------------
# Author : Sarvar  --  Group A, Smart Warehouse Project
# Role   : Status Reporting (Slot #6, Function 2)
#
# Purpose:
#   Subscribes to multiple system topics (robot velocity, tracked targets,
#   communication watchdog, SLAM confidence) and publishes a unified, human-
#   readable mission log. Also persists every log entry to a .txt file so the
#   team has a tangible record after the demo.
#
# Inputs (subscribed topics):
#   /cmd_vel                  geometry_msgs/Twist   -- current robot speed
#   /scout/tracked_target     std_msgs/String       -- from Function 1
#   /comm_status              std_msgs/String       -- from watchdog (teammate)
#   /slam/confidence          std_msgs/Float32      -- from SLAM (teammate)
#
# Outputs (published topics):
#   /mission/log    std_msgs/String  -- formatted snapshot, published at 1 Hz
#
# Side effect:
#   Appends every published line to ~/mission_log.txt
# =============================================================================

import os
import rospy
from std_msgs.msg import String, Float32
from geometry_msgs.msg import Twist
from datetime import datetime


class MissionLogger:
    """Aggregates fleet-wide status into a single periodic mission log line."""

    def __init__(self):
        rospy.init_node("mission_log_publisher_node", anonymous=False)

        # Latest-known values from each topic. Start with safe defaults so
        # the logger can run even before every teammate's node is alive.
        self.velocity = 0.0
        self.last_target = "NONE"
        self.comm_status = "UNKNOWN"
        self.slam_confidence = 0.0

        # Mission start time -- used to print elapsed seconds in the log.
        self.start_time = rospy.Time.now()

        # Output file path. Lives in the user's home folder so graders can
        # find it easily after the run.
        self.log_path = os.path.expanduser("~/mission_log.txt")
        # Truncate any old log at startup so each run is self-contained.
        with open(self.log_path, "w") as fh:
            fh.write("=== Smart Warehouse Mission Log ===\n")

        # Publisher -- created first to avoid missing the first publish tick.
        self.log_pub = rospy.Publisher("/mission/log", String, queue_size=10)

        # Subscribers -- one per upstream input.
        rospy.Subscriber("/cmd_vel", Twist, self.velocity_callback)
        rospy.Subscriber(
            "/scout/tracked_target", String, self.target_callback
        )
        rospy.Subscriber("/comm_status", String, self.comm_callback)
        rospy.Subscriber("/slam/confidence", Float32, self.slam_callback)

        # Timer: publish a consolidated log line every 1.0 s (1 Hz).
        rospy.Timer(rospy.Duration(1.0), self.publish_log)

        rospy.loginfo("[MissionLogger] Ready -- writing to %s", self.log_path)

    # -------------------------------------------------------------------------
    # CALLBACKS  --  each just caches the latest value
    # -------------------------------------------------------------------------
    def velocity_callback(self, msg):
        """Cache the linear x velocity from /cmd_vel."""
        self.velocity = msg.linear.x

    def target_callback(self, msg):
        """Cache the latest tracked target string."""
        self.last_target = msg.data

    def comm_callback(self, msg):
        """Cache the current comm watchdog status (OK / DEGRADED / LOST)."""
        self.comm_status = msg.data

    def slam_callback(self, msg):
        """Cache the SLAM mapping confidence (0.0 - 1.0)."""
        self.slam_confidence = msg.data

    # -------------------------------------------------------------------------
    # TIMER CALLBACK -- assembles and publishes the periodic log line
    # -------------------------------------------------------------------------
    def publish_log(self, _event):
        elapsed = (rospy.Time.now() - self.start_time).to_sec()
        wallclock = datetime.now().strftime("%H:%M:%S")

        line = (
            f"[T+{elapsed:6.1f}s | {wallclock}] "
            f"speed={self.velocity:+.2f} m/s | "
            f"target={self.last_target} | "
            f"comm={self.comm_status} | "
            f"slam_conf={self.slam_confidence:.2f}"
        )

        # Publish to the ROS topic so other nodes (e.g. dashboard) can see it.
        self.log_pub.publish(line)

        # Persist to disk as well -- gives us a tangible deliverable.
        with open(self.log_path, "a") as fh:
            fh.write(line + "\n")

        rospy.loginfo(line)


def main():
    try:
        MissionLogger()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("[MissionLogger] Shutting down cleanly.")


if __name__ == "__main__":
    main()
