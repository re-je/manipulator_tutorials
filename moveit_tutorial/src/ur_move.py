#!/usr/bin/env python

import sys
import math
import rospy
import moveit_commander
import tf
import geometry_msgs.msg
from ar_track_alvar_msgs.msg import AlvarMarkers

mPose = 0

def marker_cb(msg):
	global mPose
	for marker in msg.markers:
		#print "marker id: "
		#print marker.id 
		if marker.id == 1:
		    mPose = marker.pose
		    #print mPose.pose

if __name__ == '__main__':
    rospy.init_node('ur_move', anonymous=True)

    try:
        moveit_commander.roscpp_initialize(sys.argv)
        robot = moveit_commander.RobotCommander()
        group = moveit_commander.MoveGroupCommander("manipulator")
        rospy.Subscriber("ar_pose_marker", AlvarMarkers, marker_cb)

        print "Printing group names: "
        print robot.get_group_names()

        pose_target = geometry_msgs.msg.Pose()
        #pose_target.orientation.w = 1.0
        pose_target.position.x = 0.134
        pose_target.position.y = 0.224
        pose_target.position.z = 0.35

        quaternion = tf.transformations.quaternion_from_euler(0, math.pi / 2.0, 0)
        pose_target.orientation.x = quaternion[0]
        pose_target.orientation.y = quaternion[1]
        pose_target.orientation.z = quaternion[2]
        pose_target.orientation.w = quaternion[3]

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

        #moveit_commander.roscpp_shutdown()
    except rospy.ROSInterruptException:
        pass

