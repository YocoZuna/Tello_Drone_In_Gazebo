#!/bin/bash

source /opt/ros/eloquent/setup.sh
export GAZEBO_MODEL_DATABASE_URI=
gazebo --verbose /opt/ros/eloquent/share/gazebo_plugins/worlds/gazebo_ros_diff_drive_demo.world
