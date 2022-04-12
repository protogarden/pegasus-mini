import rospy 
import tf
import tf2_ros
import tf2_geometry_msgs
import geometry_msgs.msg
import std_msgs.msg
from nav_msgs.msg  import Odometry
from geometry_msgs.msg import Point, Twist, PoseStamped, Pose
from tf.transformations import euler_from_quaternion 
from math import atan2
import math

docking_tag_name = 'TAG-1' #bases_link currently for testing
base_link_frame = 'base_link'
stage_dist = 0.8
angle_thresh = 0.02

x_pose = 0
y_pose = 0

def pose_update():

    pose.header.stamp = rospy.Time(0)
    try:
        transform = tf_buffer.lookup_transform(base_link_frame,
                                    # source frame:
                                    pose.header.frame_id,
                                    # get the tf at the time the pose was valids
                                    pose.header.stamp,
                                    # wait for at most 1 second for transform, otherwise throw
                                    rospy.Duration(1))

        pose_transformed = tf2_geometry_msgs.do_transform_pose(pose, transform)

        x_pose = pose_transformed.pose.position.x
        y_pose = pose_transformed.pose.position.y
        

    
        

    except:
        speed.linear.x = 0
        speed.angular.z = 0
        pub.publish(speed)
      
        rospy.loginfo("NO TAG TF")
  

    return x_pose, y_pose

if __name__ == '__main__':
    rospy.init_node('docking_node')
    pub =rospy.Publisher("/cmd_vel",Twist,  queue_size=1)
    t = tf.TransformListener()
    rate = rospy.Rate(10)
    speed = Twist()

    pose = PoseStamped()
    pose.header = std_msgs.msg.Header()
    
    pose.header.frame_id = docking_tag_name
    pose.pose = Pose()
    pose.pose.position.x = 0
    pose.pose.position.y = 0
    pose.pose.position.z = stage_dist
    pose.pose.orientation.w = 1


    speed.linear.x = 0
    speed.angular.z = 0
    pub.publish(speed)
    

    tf_buffer = tf2_ros.Buffer(rospy.Duration(100.0))  # tf buffer length
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    # send PoseStamped
    
    while not rospy.is_shutdown():


        pose.header.stamp = rospy.Time(0)

        try:
            transform = tf_buffer.lookup_transform(base_link_frame,
                                        # source frame:
                                        pose.header.frame_id,
                                        # get the tf at the time the pose was valids
                                        pose.header.stamp,
                                        # wait for at most 1 second for transform, otherwise throw
                                        rospy.Duration(1))

            pose_transformed = tf2_geometry_msgs.do_transform_pose(pose, transform)

            x_pose = pose_transformed.pose.position.x
            y_pose = pose_transformed.pose.position.y

        
          
    
        except:
            rospy.loginfo("NO TAG TF")
            speed.linear.x = 0
            speed.angular.z = 0
            pub.publish(speed)
            
            continue
        

     
        


        try:
            (trans,rot) = t.lookupTransform( base_link_frame, docking_tag_name, rospy.Time(0))
            print("Translation")
            print(trans) 
            print("Rotation")
            print(rot)
            
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        angle_diff = math.atan(y_pose/x_pose)
        print("x_pose",x_pose)
        

        while x_pose > 0:

            x_pose, y_pose = pose_update()
            angle_diff = math.atan(y_pose/x_pose)
            print("x_pose",x_pose)
            print("angle_diff",angle_diff)

            if angle_diff < -angle_thresh:
                speed.linear.x = 0.0
                speed.angular.z = -0.05
                print("Turning Right")

            elif angle_diff > angle_thresh:
                speed.linear.x = 0.0
                speed.angular.z = 0.05
                print("Turning Left")

            else:
                speed.linear.x = 0.1
                speed.angular.z = 0

                print("Straight")

            pub.publish(speed)

      


        print("staging complete")
        speed.linear.x = 0
        speed.angular.z = 0
        pub.publish(speed)
        rate.sleep()

    speed.linear.x = 0.0
    speed.angular.z = 0.0
    pub.publish(speed)
    print("here")
