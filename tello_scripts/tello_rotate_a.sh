#!/bin/bash

source /opt/ros/eloquent/setup.sh
cd ~/tello_ros_ws
source install/setup.bash
ros2 topic pub /drone1/cmd_vel geometry_msgs/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.01}}"
