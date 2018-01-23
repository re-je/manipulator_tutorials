#!/usr/bin/env python

import sys
import math
import rospy
import moveit_commander
import tf
import geometry_msgs.msg
from ar_track_alvar_msgs.msg import AlvarMarkers
from tf import TransformListener

mPose = 0
tf_listener = 0

def handle_marker(marker_pose, target_frame):
	global tf_listener
	#print "frame_id: ", marker_pose.header.frame_id
	#print marker_pose
	marker_pose.pose.header.frame_id = marker_pose.header.frame_id 
	
	#transform pose from camera frame to base frame
	t = marker_pose.pose.pose.position
	r = marker_pose.pose.pose.orientation
	cam_to_target = tf_listener.fromTranslationRotation([t.x, t.y, t.z], [r.x, r.y, r.z, r.w])

	#if tf_listener.frameExists(target_frame) and tf_listener.frameExists(marker_pose.header.frame_id):
	t = tf_listener.getLatestCommonTime(target_frame, marker_pose.header.frame_id)
	if tf_listener.canTransform(target_frame, marker_pose.header.frame_id, t):
		res_pose = tf_listener.transformPose(target_frame, marker_pose.pose)
		#return get_marker_poseResponse(res_pose.pose)
		return res_pose		
	else:
		print "Cannot transform pose to the requsted frame"		
	#else: 
	#	print "transforms do not exist"
	return marker_pose.pose

def marker_cb(msg):
	global mPose
	for marker in msg.markers: 
		if marker.id == 1:
			res_pose = handle_marker(marker, "/world")
			mPose = res_pose

if __name__ == '__main__':
	global tf_listener
	rospy.init_node('ur_move', anonymous=True)
	tf_listener = TransformListener()
	
	try:
		moveit_commander.roscpp_initialize(sys.argv)
		robot = moveit_commander.RobotCommander()
		group = moveit_commander.MoveGroupCommander("arm")
		rospy.Subscriber("ar_pose_marker", AlvarMarkers, marker_cb)
		print group.get_pose_reference_frame()
		
		pose_target = geometry_msgs.msg.Pose()
		pose_target.position.x = 0.4
		pose_target.position.y = 0.0
		pose_target.position.z = 0.1
		
		quaternion = tf.transformations.quaternion_from_euler(0, math.pi / 2.0, 0)
		pose_target.orientation.x = 0 #quaternion[0]
		pose_target.orientation.y = 0 #quaternion[1]
		pose_target.orientation.z = 0 #quaternion[2]
		pose_target.orientation.w = 1 #quaternion[3]
		
		group.set_pose_target(pose_target)
		
		plan1 = group.plan()
		rospy.sleep(2)
		group.go(wait=True)
		
		while not rospy.is_shutdown():
			print "fetch marker [y]?"
			user = raw_input()
			if not user: break
			if user == "y" and mPose != 0:
				pose_target.position.x = mPose.pose.position.x
				pose_target.position.y = mPose.pose.position.y
				#pose_target.position.z = mPose.pose.position.z
				print pose_target
				group.set_pose_target(pose_target)
				plan1 = group.plan()
				rospy.sleep(2)
				group.go(wait=True)
				rospy.sleep(1.)
			
	except rospy.ROSInterruptException:
		pass

