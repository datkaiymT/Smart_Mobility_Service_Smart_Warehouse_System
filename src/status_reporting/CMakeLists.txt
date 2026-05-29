# =============================================================================
# CMakeLists.txt -- ROS1 Noetic build configuration for status_reporting
# -----------------------------------------------------------------------------
# Author: Sarvar -- Slot #6, Group A Smart Warehouse Project
#
# This package contains Python-only nodes (no C++ build needed). We declare
# the catkin dependencies, install the scripts so they are runnable via
# `rosrun status_reporting <node>.py`, and register the pytest suite so it
# can be invoked via `catkin_make run_tests`.
# =============================================================================

cmake_minimum_required(VERSION 3.0.2)
project(status_reporting)

# -----------------------------------------------------------------------------
# Catkin dependencies -- everything our Python nodes import from ROS.
# -----------------------------------------------------------------------------
find_package(catkin REQUIRED COMPONENTS
    rospy
    std_msgs
    geometry_msgs
)

# -----------------------------------------------------------------------------
# Declare this as a catkin package so other packages can find it.
# -----------------------------------------------------------------------------
catkin_package(
    CATKIN_DEPENDS rospy std_msgs geometry_msgs
)

# -----------------------------------------------------------------------------
# Install the Python node scripts so they are executable via rosrun and
# discoverable from launch files. The PROGRAMS keyword preserves +x bits.
# -----------------------------------------------------------------------------
catkin_install_python(PROGRAMS
    scripts/target_tracker_node.py
    scripts/mission_log_publisher_node.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# -----------------------------------------------------------------------------
# Install launch files so they can be located by roslaunch.
# -----------------------------------------------------------------------------
install(DIRECTORY launch/
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

# -----------------------------------------------------------------------------
# Pytest integration -- runs the test suite when `catkin_make run_tests`
# is invoked. Only registered if testing is enabled in the workspace.
# -----------------------------------------------------------------------------
if(CATKIN_ENABLE_TESTING)
    find_package(rostest REQUIRED)
    catkin_add_nosetests(test/test_status_reporting.py)
endif()
