import rospy 
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from actionlib_msgs.msg import GoalStatusArray
from move_base_msgs.msg import MoveBaseActionGoal
import time 

import tf
import tf2_ros
from tf.transformations import quaternion_from_euler



class StocktakeInterface():
    def __init__(self):
        self.status = 0
        self.initial_position = [0,0,0]
        self.pos_1 = [2,-1,0]
        self.pos_2 = [1,-1,3,14159]
        self.dock_pos = [0,0,0]
        
 


    def status_callback(self, data):

        if len(data.status_list) == 0:
            return

        else:
            print("status:", data.status_list[0].status)
            #1-Moving to Goal, 3- Goal Reached
           
            self.status = data.status_list[0].status
        
            print("status_text:", data.status_list[0].text)
 
        

    def goal_pose(self, goal_x, goal_y, goal_thetha):
        goal_pose_data = MoveBaseActionGoal()
        goal_pose_data.goal.target_pose.header.frame_id = 'map' 
        goal_pose_data.header.stamp = rospy.Time.now()
        goal_pose_data.goal.target_pose.pose.position.x = goal_x
        goal_pose_data.goal.target_pose.pose.position.y = goal_y
        goal_pose_data.goal.target_pose.pose.position.z = 0
        q = quaternion_from_euler(0, 0, goal_thetha)
        goal_pose_data.goal.target_pose.pose.orientation.x = 0
        goal_pose_data.goal.target_pose.pose.orientation.y = 0
        goal_pose_data.goal.target_pose.pose.orientation.z = q[2]
        goal_pose_data.goal.target_pose.pose.orientation.w = q[3]
        self.goal_pose_pub.publish(goal_pose_data)

    def estimate_pose(self, est_x, est_y, est_thetha):
        pose_estimate_data = PoseWithCovarianceStamped()
        pose_estimate_data.header.frame_id = 'map' 
        pose_estimate_data.header.stamp = rospy.Time.now()
        pose_estimate_data.pose.pose.position.x = est_x
        pose_estimate_data.pose.pose.position.y = est_y
        pose_estimate_data.pose.pose.position.z = 0.0
        q = quaternion_from_euler(0.0, 0.0, est_thetha)
        pose_estimate_data.pose.pose.orientation.x = 0.0
        pose_estimate_data.pose.pose.orientation.y = 0.0
        pose_estimate_data.pose.pose.orientation.z = q[2]
        pose_estimate_data.pose.pose.orientation.w = q[3]
        pose_estimate_data.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787]
        self.pose_estimate_pub.publish(pose_estimate_data)
        

    def run(self):
        rospy.init_node('stocktake_cmd_node', anonymous=True)
        self.goal_pose_pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=5)
        self.pose_estimate_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=5)
        rospy.Subscriber("/move_base/status", GoalStatusArray, self.status_callback, queue_size=1)
        rate = rospy.Rate(20)

        while not rospy.is_shutdown():
            
            time.sleep(1)
            self.estimate_pose(self.initial_position[0], self.initial_position[1], self.initial_position[2])
            self.goal_pose(self.pos_1[0], self.pos_1[1], self.pos_1[2])
            time.sleep(2)
            print("status",self.status)
            while self.status != 3:
                print("going to pos 1")
                rate.sleep()
            print("goal_reached")
            self.goal_pose(self.pos_2[0], self.pos_2[1], self.pos_2[2])
            time.sleep(2)
            while self.status != 3:
                print("going to pos 2")
                rate.sleep()
            print("goal_reached")
            break

            





if __name__ == '__main__':
    
    st_interface = StocktakeInterface()

    try:
        
        st_interface.run()

    except rospy.ROSInterruptException:
        pass
    
    hw_interface.stop()



 
