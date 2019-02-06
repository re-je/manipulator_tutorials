#!/usr/bin/env python

import sys
import rospy
import moveit_commander
import tf
from geometry_msgs.msg import Pose
from ar_track_alvar_msgs.msg import AlvarMarkers

#declare global variables
world_frame = rospy.get_param('~/world_frame', "world")
vel_scaling = rospy.get_param('~/vel_scaling', .3)
home_position = rospy.get_param('~/home_position', [.4, .0, .3])
home_orientation = rospy.get_param('~/home_orientation', [.0, .0, .0, .1])
marker_pose = None

#convert marker from camera frame to robot's base frame
def transform_pose(pose, target_frame):
	if tf_listener.canTransform(target_frame, pose.header.frame_id, rospy.Time(0)):
		#transform pose
		return transform.pose

#callback function to receive marker messages
def marker_cb(msg):
	global marker_pose
	if len(msg.markers) == 0:
		return
	marker = msg.markers[0]
	marker.pose.header.frame_id = marker.header.frame_id
	marker_pose = transform_pose(marker.pose, world_frame)

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
	#set pose target
	#plan
	if plan_accepted():
		#execute
	else:
		exit()

#main function of application
def main():
	#initialize moveit
	moveit_commander.roscpp_initialize(sys.argv)

	group = moveit_commander.MoveGroupCommander("move_group_name")
	group.set_max_velocity_scaling_factor(vel_scaling)

	#while loop to move the robot to the found AR marker
	while not rospy.is_shutdown():
		plan_and_execute(group, set_pose(home_position, home_orientation))
		if marker_pose:
			marker = [marker_pose.position.x, marker_pose.position.y, home_position[2]]
			plan_and_execute(group, set_pose(marker))
		else:
			rospy.logwarn("No marker detected.")

if __name__ == '__main__':
	rospy.init_node('move_to_marker', anonymous=True)
	tf_listener = tf.TransformListener()
	rospy.Subscriber("ar_pose_marker", AlvarMarkers, marker_cb)

	main()
