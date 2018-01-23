#!/usr/bin/env python

import sys
import math
import rospy
import moveit_commander
import tf
import geometry_msgs.msg
from ar_track_alvar_msgs.msg import AlvarMarkers
from tf import TransformListener

#declare global variables
mPose = 0
tf_listener = 0
marker_id = -1

#convert marker from camera frame to robot's base frame
def handle_marker(marker_pose, target_frame):
	global tf_listener
	
	marker_pose.pose.header.frame_id = marker_pose.header.frame_id 
	
	#transform pose from camera frame to base frame
	t = marker_pose.pose.pose.position
	r = marker_pose.pose.pose.orientation
	cam_to_target = tf_listener.fromTranslationRotation([t.x, t.y, t.z], [r.x, r.y, r.z, r.w])

	t = tf_listener.getLatestCommonTime(target_frame, marker_pose.header.frame_id)
	if tf_listener.canTransform(target_frame, marker_pose.header.frame_id, t):
		res_pose = tf_listener.transformPose(target_frame, marker_pose.pose)
		return res_pose		
	else:
		print "Cannot transform pose to the requsted frame"		
	#else: 
	#	print "transforms do not exist"
	return marker_pose.pose

#call back function to receive marker messages
def marker_cb(msg):
	global mPose
	for marker in msg.markers: 
		#check marker.id on /ar_pose_marker topic
		if marker.id == marker_id:
			res_pose = handle_marker(marker, "/world")
			mPose = res_pose

def plan_and_execute(pose):
	group.set_pose_target(pose)
		
	#plan and execute using Moveit!
	plan1 = group.plan()
	rospy.sleep(2)
	group.go(wait=True)

if __name__ == '__main__':
	global tf_listener
	rospy.init_node('ur_move', anonymous=True)
	tf_listener = TransformListener()
	
	#get marker id passed through the command line
	marker_id = int(sys.argv[1])
	
	try:
		#initialize necessary objects
		moveit_commander.roscpp_initialize(sys.argv)
		robot = moveit_commander.RobotCommander()
		group = moveit_commander.MoveGroupCommander("arm")
		rospy.Subscriber("ar_pose_marker", AlvarMarkers, marker_cb)
		print group.get_pose_reference_frame()
		
		#set robot to home position 
		pose_home = geometry_msgs.msg.Pose()
		pose_home.position.x = 0.4
		pose_home.position.y = 0.0
		pose_home.position.z = 0.3
		
		pose_home.orientation.x = 0 
		pose_home.orientation.y = 0 
		pose_home.orientation.z = 0 
		pose_home.orientation.w = 1 
		
		plan_and_execute(pose_home)

		#while loop to move the robot to the found AR marker
		pose_target = geometry_msgs.msg.Pose()
		while not rospy.is_shutdown():
			print "fetch marker [y]?"
			user = raw_input()
			if not user: break
			if user == "y" and mPose != 0:
				pose_target.position.x = mPose.pose.position.x
				pose_target.position.y = mPose.pose.position.y
				pose_target.position.z = pose_home.position.z
				pose_target.orientation = pose_home.orientation
				print pose_target

				plan_and_execute(pose_target)
				rospy.sleep(1.)
				plan_and_execute(pose_home)
				rospy.sleep(1.)
			
	except rospy.ROSInterruptException:
		pass

