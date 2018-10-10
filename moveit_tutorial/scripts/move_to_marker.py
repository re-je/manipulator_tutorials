#!/usr/bin/env python

import sys
import rospy
import moveit_commander
import tf
from geometry_msgs.msg import Pose
from ar_track_alvar_msgs.msg import AlvarMarkers

#declare global variables
world_frame = rospy.get_param('~/world_frame', "world")
#Task 1: Add the correct default group name in place of "???" below
#        Refer to Rviz to get the group name
move_group_name = "???"
vel_scaling = rospy.get_param('~/vel_scaling', .3)
home_position = rospy.get_param('~/home_position', [.4, .0, .3])
home_orientation = rospy.get_param('~/home_orientation', [.0, .0, .0, .1])
marker_pose = None

#convert marker from camera frame to robot's base frame
def transform_pose(pose, target_frame):
	if tf_listener.canTransform(target_frame, pose.header.frame_id, rospy.Time(0)):
		transform = tf_listener.transformPose(target_frame, pose)
		return transform.pose
	else:
		rospy.logerr("Transform not successfull.")
		return False

#callback function to receive marker messages
def marker_cb(msg):
	global marker_pose
	for marker in msg.markers:
		if marker.id == marker_id: #check marker.id on /ar_pose_marker topic
			marker.pose.header.frame_id = marker.header.frame_id
			pose_local = transform_pose(marker.pose, world_frame)
			if pose_local:
				marker_pose = pose_local

#set Pose message through lists
def set_pose(xyz = [0, 0, 0], q = [0, 0, 0, 1]):
	pose = Pose()
	pose.position.x, pose.position.y, pose.position.z = xyz
	pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w = q
	return pose

#confirm if plan should be executed
def plan_accepted():
	return raw_input("Do you want to execute the plan [y] or replan [n]? ") == "y"

#plan and execute to given pose; If plan is not confirmed plan again
def plan_and_execute(group, pose):
	group.set_pose_target(pose)
	plan1 = group.plan()
	if plan_accepted():
		group.execute(plan1, wait=True)
	else:
		plan_and_execute(group, pose)

#main function of application
def main():
	#initialize moveit
	moveit_commander.roscpp_initialize(sys.argv)
	robot = moveit_commander.RobotCommander()
	group = moveit_commander.MoveGroupCommander(move_group_name)
	group.set_max_velocity_scaling_factor(vel_scaling)

	#while loop to move the robot to the found AR marker
	while not rospy.is_shutdown():
		plan_and_execute(group, set_pose(home_position, home_orientation))
		if marker_pose:
			#Task 3: Assign x & y position values from "marker_pose" to "marker"
			#        HINT: "marker_pose" is using the message type 'geometry_msgs/Pose'
			marker = [marker_pose.???, marker_pose.???, home_position[2]]
			plan_and_execute(group, set_pose(marker))
		else:
			rospy.logwarn("No marker detected.")

if __name__ == '__main__':
	rospy.init_node('move_to_marker', anonymous=True)
	tf_listener = tf.TransformListener()
	#Task 2: Modify the following subscriber to the correct ar marker pose topic &
	#        the correct message type. HINT: Check the topic from the command line
	rospy.Subscriber("topic_name?", msg_type?, marker_cb)
	#get marker id passed through the command line
	argv = rospy.myargv()
	if len(argv) == 1:
		rospy.logerr("Node requires an argument for the marker_id.")
		sys.exit(1)
	else:
		marker_id = int(sys.argv[1])
	main()
