cmake_minimum_required(VERSION 3.0.2)
project(package_verification)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/package_verification_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)