# ############################################################################
#
#    ┌──┬──┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┬────┐        ▒▒▒▒▒░░░░░▓▓▓▓▓
#    │  │  │ ├─────┤ └─────┐ │       │     │ ├───┬┘        FH Aachen
#    ┘     └ ┘     └ └─────┘ └─────┘ └─────┘ ┘   └─        University of
#    Mobile Autonomous Systems & Cognitive Robotics        Applied Sciences
#
# ############################################################################
#
#  description: tf2_listener.py
#    author(s): Stefan Schiffer
#      license: CC-BY-ND
#
# ############################################################################

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
        trans = tfBuffer.lookup_transform("turtle2", "turtle1", rospy.Time(0))
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        continue

    cmd.linear.x = 0.5 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2)
    cmd.angular.z = 4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
    turtle_vel.publish(cmd)
    r.sleep()
