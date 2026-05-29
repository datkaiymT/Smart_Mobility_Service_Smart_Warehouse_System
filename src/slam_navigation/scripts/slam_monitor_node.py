#!/usr/bin/env python3
"""
slam_monitor_node.py
--------------------
SLAM Navigation Monitor for Smart Warehouse Autonomous Mobility System.

Responsibilities:
  - Subscribes to /map (OccupancyGrid) and /scan (LaserScan)
  - Computes map confidence score from known vs unknown cells
  - Publishes confidence score to /slam/confidence
  - Triggers watchdog alert if confidence drops below threshold
  - Integrates with eco_router via /cmd_vel subscription

Author: Datkaiym
"""

import rospy
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32, Bool


class SlamMonitorNode:
    def __init__(self):
        rospy.init_node("slam_monitor_node", anonymous=False)

        # Parameters
        self.map_update_interval   = rospy.get_param("~map_update_interval", 2.0)
        self.low_conf_threshold    = rospy.get_param("~low_confidence_threshold", 0.3)

        # Internal state
        self.latest_confidence     = 0.0
        self.latest_velocity       = 0.0
        self.map_received          = False

        # Publishers
        self.confidence_pub  = rospy.Publisher("/slam/confidence",      Float32, queue_size=10)
        self.alert_pub       = rospy.Publisher("/slam/low_confidence_alert", Bool, queue_size=10)

        # Subscribers
        rospy.Subscriber("/map",      OccupancyGrid, self.map_callback)
        rospy.Subscriber("/scan",     LaserScan,     self.scan_callback)
        rospy.Subscriber("/cmd_vel",  Twist,         self.velocity_callback)

        # Timer — publish confidence at fixed interval
        rospy.Timer(
            rospy.Duration(self.map_update_interval),
            self.publish_confidence
        )

        rospy.loginfo("[SLAM Monitor] Node initialized. Waiting for map data...")
        rospy.spin()

    # ------------------------------------------------------------------
    def map_callback(self, msg: OccupancyGrid):
        """
        Compute confidence as the ratio of known cells (0 or 100)
        to total cells. Unknown cells have value -1.
        """
        total_cells = len(msg.data)
        if total_cells == 0:
            self.latest_confidence = 0.0
            return

        known_cells = sum(1 for cell in msg.data if cell != -1)
        self.latest_confidence = known_cells / total_cells
        self.map_received = True

        rospy.logdebug(
            f"[SLAM Monitor] Map updated — "
            f"known={known_cells}/{total_cells} "
            f"confidence={self.latest_confidence:.2f}"
        )

    # ------------------------------------------------------------------
    def scan_callback(self, msg: LaserScan):
        """
        Log laser scan range summary for diagnostics.
        Filters out inf and nan values before computing stats.
        """
        valid_ranges = [r for r in msg.ranges if not (r != r) and r != float("inf")]
        if valid_ranges:
            rospy.logdebug(
                f"[SLAM Monitor] Scan — "
                f"min={min(valid_ranges):.2f}m  "
                f"max={max(valid_ranges):.2f}m  "
                f"points={len(valid_ranges)}"
            )

    # ------------------------------------------------------------------
    def velocity_callback(self, msg: Twist):
        """
        Track current platform velocity published by move_base.
        This feeds into eco-router awareness.
        """
        self.latest_velocity = msg.linear.x
        rospy.logdebug(f"[SLAM Monitor] Velocity received: {self.latest_velocity:.3f} m/s")

    # ------------------------------------------------------------------
    def publish_confidence(self, event):
        """
        Timer callback — publishes confidence score and fires alert
        if score drops below the safety threshold.
        """
        if not self.map_received:
            rospy.logwarn("[SLAM Monitor] No map received yet.")
            return

        self.confidence_pub.publish(Float32(self.latest_confidence))

        is_low = self.latest_confidence < self.low_conf_threshold
        self.alert_pub.publish(Bool(is_low))

        if is_low:
            rospy.logwarn(
                f"[SLAM Monitor] LOW CONFIDENCE ALERT: "
                f"{self.latest_confidence:.2f} < threshold {self.low_conf_threshold}"
            )
        else:
            rospy.loginfo(
                f"[SLAM Monitor] Confidence OK: {self.latest_confidence:.2f} | "
                f"Velocity: {self.latest_velocity:.2f} m/s"
            )


# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        SlamMonitorNode()
    except rospy.ROSInterruptException:
        rospy.loginfo("[SLAM Monitor] Node shut down cleanly.")