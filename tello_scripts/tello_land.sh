#!/bin/bash

source /opt/ros/eloquent/setup.sh
cd ~/tello_ros_ws
source install/setup.bash
ros2 service call /drone1/tello_action tello_msgs/TelloAction "{cmd: 'land'}"
