cmake_minimum_required(VERSION 3.0.2)
project(cli_manager)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

# 1. Setup Python
catkin_python_setup()

# 2. Add and Generate Messages
add_message_files(
  FILES
  RobotStatus.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

# 3. Finalize package configuration
catkin_package(
  CATKIN_DEPENDS rospy std_msgs message_runtime
)