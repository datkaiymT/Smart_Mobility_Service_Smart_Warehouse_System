#!/usr/bin/env python3
# =============================================================================
# target_tracker_node.py
# -----------------------------------------------------------------------------
# Author : Sarvar  --  Group A, Smart Warehouse Project
# Role   : Status Reporting (Slot #6, Function 1)
#
# Purpose:
#   Subscribes to raw detections coming from the Scout robot's perception node
#   and maintains a stable, time-stamped record of each detected target. Acts
#   as the "memory" between transient detections and downstream consumers
#   (mission logger, coordinator, dashboard).
#
# Inputs  (subscribed topics):
#   /scout/detections   std_msgs/String   -- e.g. "BlueBox,0.87,2.3,1.1"
#                                            (label, confidence, x, y)
#
# Outputs (published topics):
#   /scout/tracked_target   std_msgs/String  -- formatted tracked target info
#   /scout/target_count     std_msgs/Int32   -- how many unique targets seen
# =============================================================================

import rospy
from std_msgs.msg import String, Int32
from datetime import datetime


class TargetTracker:
    """Tracks unique targets detected by the Scout robot."""

    def __init__(self):
        # Initialize the ROS node. anonymous=False because we only want one
        # tracker running in the fleet at any time.
        rospy.init_node("target_tracker_node", anonymous=False)

        # Internal memory of seen targets. Key = label string, Value = dict
        # holding confidence, position, and last-seen timestamp.
        self.tracked = {}

        # Publishers -- created BEFORE the subscriber so we never miss the
        # first detection arriving immediately after startup.
        self.tracked_pub = rospy.Publisher(
            "/scout/tracked_target", String, queue_size=10
        )
        self.count_pub = rospy.Publisher(
            "/scout/target_count", Int32, queue_size=10
        )

        # Subscriber to the raw detection feed.
        rospy.Subscriber("/scout/detections", String, self.detection_callback)

        rospy.loginfo("[TargetTracker] Node ready -- waiting for detections.")

    # -------------------------------------------------------------------------
    # CALLBACKS
    # -------------------------------------------------------------------------
    def detection_callback(self, msg):
        """
        Triggered every time a new raw detection arrives.
        Expected format: "label,confidence,x,y"
        """
        try:
            parts = msg.data.split(",")
            label = parts[0].strip()
            confidence = float(parts[1])
            x = float(parts[2])
            y = float(parts[3])
        except (IndexError, ValueError) as err:
            # Malformed input -- log and move on. We do not crash the node
            # because the test rubric expects resilient behavior.
            rospy.logwarn("[TargetTracker] Bad detection ignored: %s", err)
            return

        # Update memory with the newest observation for this label.
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.tracked[label] = {
            "confidence": confidence,
            "x": x,
            "y": y,
            "last_seen": timestamp,
        }

        # Publish a human-readable tracked target string.
        out = (
            f"[{timestamp}] Tracked={label} "
            f"conf={confidence:.2f} pos=({x:.2f},{y:.2f})"
        )
        self.tracked_pub.publish(out)
        self.count_pub.publish(Int32(len(self.tracked)))

        rospy.loginfo("[TargetTracker] %s", out)


def main():
    """Entry point. Wrapped in try/except so Ctrl+C does not dump a stacktrace."""
    try:
        TargetTracker()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("[TargetTracker] Shutting down cleanly.")


if __name__ == "__main__":
    main()