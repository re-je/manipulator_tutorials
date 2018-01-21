#!/usr/bin/env python

import sys
import math
import rospy
import moveit_commander
import tf
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('denso_move', anonymous=True)

    try:
        moveit_commander.roscpp_initialize(sys.argv)
        robot = moveit_commander.RobotCommander()
        group = moveit_commander.MoveGroupCommander("arm")

        print "Printing group names: "
        print robot.get_group_names()

        pose_target = geometry_msgs.msg.Pose()
        #pose_target.orientation.w = 1.0
        pose_target.position.x = 0.5
        pose_target.position.y = 0
        pose_target.position.z = 0.4

        quaternion = tf.transformations.quaternion_from_euler(0, math.pi, 0)
        pose_target.orientation.x = quaternion[0]
        pose_target.orientation.y = quaternion[1]
        pose_target.orientation.z = quaternion[2]
        pose_target.orientation.w = quaternion[3]

        group.set_pose_target(pose_target)

        plan1 = group.plan()
        rospy.sleep(2)
        group.go(wait=True)

        moveit_commander.roscpp_shutdown()
    except rospy.ROSInterruptException:
        pass

