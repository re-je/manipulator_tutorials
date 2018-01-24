# ############################################################################
#
#    ┌──┬──┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┬────┐        ▒▒▒▒▒░░░░░▓▓▓▓▓
#    │  │  │ ├─────┤ └─────┐ │       │     │ ├───┬┘        FH Aachen
#    ┘     └ ┘     └ └─────┘ └─────┘ └─────┘ ┘   └─        University of
#    Mobile Autonomous Systems & Cognitive Robotics        Applied Sciences
#
# ############################################################################
#
#  description: tf2_broadcaster.py
#    author(s): Stefan Schiffer
#      license: CC-BY-ND
#
# ############################################################################

#!/usr/bin/env python

# import
import rospy
import tf2_ros
import tf_conversions
import geometry_msgs.msg
from turtlesim.msg import Pose

# node initialization
rospy.init_node("tf_bc_exmpl")

# variable definition
br = tf2_ros.TransformBroadcaster()
t = geometry_msgs.msg.TransformStamped()
r = rospy.Rate(30)
turtle_name = rospy.get_param("~turtle")

# definition of functions
def handle_turtle_pose(msg):
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "world"
    t.child_frame_id = turtle_name
    t.transform.translation.x = msg.x
    t.transform.translation.y = msg.y
    t.transform.translation.z = 0.0
    q = tf_conversions.transformations.quaternion_from_euler(0, 0, 	msg.theta)
    
    # Task 1: Use the correct form of TransformStamped msg 't'
    # Hint find the message format of geometry_msgs/TransformStamped from command line
    #t_x = q[0]
    #t_y = q[1]
    #t_z = q[2]
    #t_w = q[3]

rospy.Subscriber("%s/pose" % turtle_name, Pose, handle_turtle_pose)

while not rospy.is_shutdown():
    # Task 2: Use the send transform function to broadcast 't'
    # HINT: Refer link to use the correct function for TransformBroadcaster 'br'
    # http://docs.ros.org/kinetic/api/tf/html/c++/classtf_1_1TransformBroadcaster.html    
    r.sleep()
