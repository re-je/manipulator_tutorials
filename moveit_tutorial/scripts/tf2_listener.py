#!/usr/bin/env python

# import
import rospy
import math
import tf2_ros
import geometry_msgs.msg

# node initialization
rospy.init_node("tf_lstnr_exmpl")

# variable definition
cmd = geometry_msgs.msg.Twist()
tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)

# definition of publishers/subscribers/services
turtle_vel = rospy.Publisher("turtle2/cmd_vel", geometry_msgs.msg.Twist, queue_size=1)

# main program
r = rospy.Rate(30) #30Hz

while not rospy.is_shutdown():
    try:
		# Task 1: Fill the function lookup_transform with correct order of frames
		# turtle1 is source_frame
		# turtle2 is target_frame
		# HINT: Refer link to find the correct order
		# http://docs.ros.org/jade/api/tf/html/c++/classtf_1_1Transformer.html
        trans = tfBuffer.lookup_transform('some_frame', 'another_frame', rospy.Time(0))
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        continue

    cmd.linear.x = 0.5 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2)
    cmd.angular.z = 4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
    turtle_vel.publish(cmd)
    r.sleep()
