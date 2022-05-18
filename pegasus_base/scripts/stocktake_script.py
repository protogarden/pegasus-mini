import rospy 
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from actionlib_msgs.msg import GoalStatusArray
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionResult, MoveBaseAction, MoveBaseGoal
import time 
import actionlib

import tf
import tf2_ros
from tf.transformations import quaternion_from_euler
from std_msgs.msg import Int32



class StocktakeInterface():
    def __init__(self):
        self.status = 0
        self.initial_position = [0,0,0]
        self.pos_1 = [2,-1,0]
        self.pos_2 = [1,-1,3.14159]
        self.dock_pos = [0,0,0]
        self.docking_interface = 0 #1 - Dock #2 - Undock #3- Docking, #4 -Undocking,#5 - Docked, #6 - Undocked
        self.dock_cmd = 1
        self.undock_cmd = 2
      
        

    def un_dock(self):
        self.docking_interface = self.undock_cmd
        self.dock_cmd_pub.publish(self.docking_interface) #publish cmd 
        while self.docking_interface != 4: #wait for result 
            rate.sleep()
        while self.docking_interface != 6: #wait for result 
            rate.sleep()

    def dock(self):
        self.docking_interface = self.dock_cmd
        self.dock_cmd_pub.publish(self.docking_interface) #publish cmd 
        while self.docking_interface != 3: #wait for result 
            rate.sleep()
        while self.docking_interface != 5: #wait for result 
            rate.sleep()
        
        
    def docking_callback(self, data):
        self.docking_interface = data.data


    def status_callback(self, data):
        #rospy.Subscriber("/move_base/result", MoveBaseActionResult, self.status_callback, queue_size=1)

        if len(data.status_list) == 0:
            return

        else:
            print("status:", data.status_list[0].status)
            #1-Moving to Goal, 3- Goal Reached
           
            self.status = data.status_list[0].status
        
            print("status_text:", data.status_list[0].text)
 
        

    def goal_pose(self, goal_x, goal_y, goal_thetha):

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = goal_x
        goal.target_pose.pose.position.y = goal_y
        goal.target_pose.pose.position.z = 0
        q = quaternion_from_euler(0.0, 0.0, goal_thetha)
        goal.target_pose.pose.orientation.x = 0
        goal.target_pose.pose.orientation.y = 0
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3]
        self.client.send_goal(goal)

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
        #self.goal_pose_pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=5)
        self.pose_estimate_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=5)


        self.dock_cmd_pub = rospy.Publisher('/docking_interface', Int32, queue_size=1)
        rospy.Subscriber('/docking_interface',  Int32 , self.status_callback)
    
        
        rate = rospy.Rate(20)
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()
        self.estimate_pose(self.initial_position[0], self.initial_position[1], self.initial_position[2]) #Send initial Pose
        while not rospy.is_shutdown():
            
            #time.sleep(1)
            
            self.goal_pose(self.pos_1[0], self.pos_1[1], self.pos_1[2])
            time.sleep(1)
            goal_state = self.client.get_state()
            print("current_state", goal_state)
            wait = self.client.wait_for_result()
            goal_state = self.client.get_state()
            result = self.client.get_result()
            print("result",goal_state )
 
            self.goal_pose(self.pos_2[0], self.pos_2[1], self.pos_2[2])
            time.sleep(1)
            goal_state = self.client.get_state()
            print("current_state", goal_state)
            wait = self.client.wait_for_result()
            goal_state = self.client.get_state()
            result = self.client.get_result()
            print("result",goal_state )

            break

            

if __name__ == '__main__':
    
    st_interface = StocktakeInterface()

    try:
        
        st_interface.run()

    except rospy.ROSInterruptException:
        pass
    
 



 
