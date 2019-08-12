# Yaskawa GP8 MoveIt config

Working MoveIt config for demos on physical hardware.

> **CAUTION**: Remember that you should always have your hands on the big red
> button in case there is something in the way or anything unexpected happens.

## Usage

> **NOTE**: The below notes assumes a robot ip address of 192.168.255.1. Update
> this as needed

### With real Hardware

Ping the robot's ip to make sure you have working communication.

    ping 192.168.255.1

Test ROS communication by brining up a robot state visualisation in Rviz.

    roslaunch motoman_gp8_support robot_state_visualize_gp8.launch robot_ip:=192.168.255.1 controller:=yrc1000

### MoveIt! with real Hardware

Set up the MoveIt! nodes to allow motion planning.

    roslaunch motoman_gp8_moveit_config gp8_planning_execution.launch sim:=false robot_ip:=192.168.255.1

Enable the robot.

    rosservice call /robot_enable

### MoveIt! with a simulated robot

Again, you can use MoveIt! to control the simulated robot.

    roslaunch motoman_gp8_moveit_config gp8_planning_execution.launch sim:=true
