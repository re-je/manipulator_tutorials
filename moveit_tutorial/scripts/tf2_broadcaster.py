#!/usr/bin/env python  
import rospy

# Because of transformations
import tf

import tf2_ros
import geometry_msgs.msg
import turtlesim.msg


def handle_turtle_pose(msg, turtlename):
    br = tf2_ros.TransformBroadcaster()
    t = geometry_msgs.msg.TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "world"
    t.child_frame_id = turtlename
    t.transform.translation.x = msg.x
    t.transform.translation.y = msg.y
    t.transform.translation.z = 0.0
    q = tf.transformations.quaternion_from_euler(0, 0, msg.theta)

    # Task 1: Use the correct form of TransformStamped msg 't'
    # Hint find the message format of geometry_msgs/TransformStamped from command line
    t.transform.rotation.x = q[0]
    #t_y = q[1]
    #t_z = q[2]
    #t_w = q[3]

    # Task 2: Use the send transform function to broadcast 't'
    # HINT: Refer link to use the correct function for TransformBroadcaster 'br'
    # http://docs.ros.org/kinetic/api/tf/html/c++/classtf_1_1TransformBroadcaster.html 
    ???

if __name__ == '__main__':
    rospy.init_node('tf2_turtle_broadcaster')
    turtlename = rospy.get_param('~turtle')
    rospy.Subscriber('/%s/pose' % turtlename,
                     turtlesim.msg.Pose,
                     handle_turtle_pose,
                     turtlename)
    rospy.spin()
