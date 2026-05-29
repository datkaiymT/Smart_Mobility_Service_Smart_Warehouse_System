# Status Reporting Subsystem
**Group A — Smart Warehouse Coordination System**
**Member: Sarvar — Slot #6 (Target object tracking + Mission log publisher)**

---

## Overview

This subsystem provides fleet-wide situational awareness for the Smart Warehouse by tracking detected targets and publishing a unified mission log that aggregates every other subsystem's state.

## ROS Functions

| # | Node | File | Purpose |
|---|---|---|---|
| 1 | `target_tracker_node` | `scripts/target_tracker_node.py` | Maintains a stable record of all targets detected by the Scout robot |
| 2 | `mission_log_publisher_node` | `scripts/mission_log_publisher_node.py` | Aggregates velocity, target, comm, and SLAM data into a 1 Hz human-readable log |

## Topic Interface

### Subscribed
- `/scout/detections` (`std_msgs/String`) — raw detections from Perception teammate
- `/cmd_vel` (`geometry_msgs/Twist`) — robot velocity from Motion Control teammate
- `/comm_status` (`std_msgs/String`) — from Datkaiym's Communication Watchdog
- `/slam/confidence` (`std_msgs/Float32`) — from Datkaiym's SLAM Monitor

### Published
- `/scout/tracked_target` (`std_msgs/String`)
- `/scout/target_count` (`std_msgs/Int32`)
- `/mission/log` (`std_msgs/String`) — published at 1 Hz

### Side effect
- Appends every mission log line to `~/mission_log.txt` (cleared at startup of each run)

## Sample Output

```
[T+  12.3s | 14:25:01] speed=+0.40 m/s | target=BlueBox | comm=OK | slam_conf=0.85
[T+  13.3s | 14:25:02] speed=+0.42 m/s | target=BlueBox | comm=OK | slam_conf=0.87
[T+  14.3s | 14:25:03] speed=+0.00 m/s | target=BlueBox | comm=DEGRADED | slam_conf=0.81
```

## Build Instructions (ROS1 Noetic)

1. Drop this folder into your catkin workspace `src/`:
   ```
   ~/catkin_ws/src/status_reporting/
   ```

2. Make the Python nodes executable (one-time setup):
   ```bash
   chmod +x ~/catkin_ws/src/status_reporting/scripts/*.py
   ```

3. Build the workspace:
   ```bash
   cd ~/catkin_ws
   catkin_make
   source devel/setup.bash
   ```

## Run Instructions

### Standalone
```bash
# Terminal 1
roscore

# Terminal 2
roslaunch status_reporting status_reporting.launch
```

### Individual nodes (for debugging)
```bash
rosrun status_reporting target_tracker_node.py
rosrun status_reporting mission_log_publisher_node.py
```

### Integrated with master launch
Add to the team's master launch file:
```xml
<include file="$(find status_reporting)/launch/status_reporting.launch"/>
```

## Tests

Pytest scenarios validate parsing and formatting logic without requiring a live ROS master:

```bash
# Direct pytest invocation
cd test
pytest -v test_status_reporting.py
```

```bash
# Or via catkin (runs as part of the workspace test suite)
cd ~/catkin_ws
catkin_make run_tests_status_reporting
```

Test coverage:
- Valid detection parsing
- Malformed detection input is handled gracefully (no crash)
- Whitespace in labels is stripped
- Log line contains all required fields
- Negative velocity renders with explicit minus sign
- Default values render cleanly before teammates' nodes are alive

## Bag Recording

The launch file automatically records every relevant topic to `~/status_reporting_<timestamp>.bag` for replay and grading evidence.

## Integration Notes

This subsystem depends on the following topics being published by teammates:
- **Datkaiym** — `/comm_status`, `/slam/confidence`
- **Perception teammate** — `/scout/detections` (format: `label,confidence,x,y`)
- **Motion Control teammate** — `/cmd_vel`

The nodes use safe default values (`UNKNOWN`, `NONE`, `0.0`) so the logger still runs even if a teammate's node is not yet online — useful during incremental integration testing.
