import rospy 
import tf
import geometry_msgs.msg
from nav_msgs.msg  import Odometry
from geometry_msgs.msg import Point, Twist
from tf.transformations import euler_from_quaternion 
from math import atan2

docking_tag_name = '/TAG' #bases_link currently for testing
camera_frame = '/base_link'
stage_dist = 0.5
test_x = 1
test_y = 0 
thresh = 0.02




if __name__ == '__main__':
    rospy.init_node('docking_node')
    pub =rospy.Publisher("/cmd_vel",Twist,  queue_size=1)
    t = tf.TransformListener()
    rate = rospy.Rate(10)
    speed = Twist()
    print("1")
    while not rospy.is_shutdown():
        print("1")
        try:
            (trans,rot) = t.lookupTransform( camera_frame, docking_tag_name, rospy.Time(0))
            print("Translation")
            print(trans) 
            print("Rotation")
            print(rot)
            
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

    
       
        if len(trans) == 0:
            print('no tag')
            speed.linear.x = 0.0
            speed.angular.z = 0.1


        else:
            print('tag')
            if trans[1] < -thresh*3*trans[0]:
                speed.linear.x = 0.0
                speed.angular.z = -0.1

            elif trans[1] > thresh*3*trans[0]:
                speed.linear.x = 0.0
                speed.angular.z = 0.1

            else: 
                speed.linear.x = 0.1
                speed.angular.z = 0.0


        if trans[0] < 0.6 :
            speed.linear.x = 0.0

            speed.angular.z = 0.0


        pub.publish(speed)
        print('tag')
        goal = Point ()
        '''
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
        '''

        rate.sleep()

    speed.linear.x = 0.0
    speed.angular.z = 0.0
    pub.publish(speed)
    print("here")