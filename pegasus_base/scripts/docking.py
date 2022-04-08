import rospy 
import tf
import geometry_msgs.msg
from nav_msgs.msg  import Odometry
from geometry_msgs.msg import Point, Twist
from tf.transformations import euler_from_quaternion 
from math import atan2

docking_tag_name = '/odom' #bases_link currently for testing
camera_frame = '/base_link'
stage_dist = 0.5
test_x = 1
test_y = 0 




if __name__ == '__main__':
    rospy.init_node('docking_node')
    pub =rospy.Publisher("/cmd_vel",Twist,  queue_size=1)
    t = tf.TransformListener()
    rate = rospy.Rate(10)
    speed = Twist()
    while not rospy.is_shutdown():
        try:
            (trans,rot) = t.lookupTransform( camera_frame, docking_tag_name, rospy.Time(0))
            print("Translation")
            print(trans) 
            print("Rotation")
            print(rot)
            
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        roll, pitch, theta = euler_from_quaternion ([rot[0],  rot[1], rot[2], rot[3]])
       

        goal = Point ()
        goal.x = test_x -trans[0] - stage_dist
        goal.y = test_y -trans[1]

        angle_to_goal = atan2 (goal.y, goal.x)

        if (angle_to_goal) > 0:
                speed.linear.x = 0.0
                speed.angular.z = 0.5

        elif (angle_to_goal) < 0:
                speed.linear.x = 0.0
                speed.angular.z = -0.5  

        else:
                speed.linear.x = 0.2
                speed.angular.z = 0.0

        pub.publish(speed)

        rate.sleep()

    speed.linear.x = 0.0
    speed.angular.z = 0.0
    pub.publish(speed)
    print("here")