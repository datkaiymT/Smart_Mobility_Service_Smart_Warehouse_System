# SLAM Navigation – Smart Warehouse Autonomous Mobility System

Subtopic module for the Smart Warehouse project by Group A.

## Overview

This package implements SLAM-based navigation monitoring
for a warehouse autonomous mobile platform running on ROS Noetic.

It integrates with:
- `eco_router.py` via `/cmd_vel` velocity topic
- `communication_watchdog.py` via `/slam/low_confidence_alert`
- GMapping SLAM node via `/map` and `/scan`

## Topic Pipeline

| Topic                      | Type              | Direction  |
|---------------------------|-------------------|------------|
| `/scan`                   | LaserScan         | Subscribed |
| `/map`                    | OccupancyGrid     | Subscribed |
| `/cmd_vel`                | Twist             | Subscribed |
| `/slam/confidence`        | Float32           | Published  |
| `/slam/low_confidence_alert` | Bool           | Published  |

## Run

```bash
roslaunch slam_navigation slam_navigation.launch
```

## Test

```bash
cd slam_navigation/tests
pytest test_slam_monitor.py -v
```

## Dependencies

- ROS Noetic
- `gmapping` package
- `tf2_ros`
- Python 3, pytest
