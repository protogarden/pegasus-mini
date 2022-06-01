#!/usr/bin/env python
import rospy
from std_msgs.msg import String, UInt32, Int64MultiArray, Float32MultiArray,Int32, Float32
from sensor_msgs.msg import Joy
from roboclaw import Roboclaw

from geometry_msgs.msg import Quaternion, Twist
from nav_msgs.msg import Odometry
import tf
from math import pi, cos, sin
import math


class RoboClawInterface:
    def __init__(self):
        
        self.left_speed = 0
        self.right_speed = 0
        self.cur_x = 0
        self.cur_y = 0
        self.cur_theta = 0.0
        self.last_enc_left = 0
        self.last_enc_right = 0
        
        self.encoder = None
  



    def normalize_angle(angle):
        
        while angle > pi:
            angle -= 2.0 * pi
        while angle < -pi:
            angle += 2.0 * pi
        return angle

    def update(self, enc_left, enc_right):
        
        left_ticks = enc_left - self.last_enc_left
        right_ticks = enc_right - self.last_enc_right
        self.last_enc_left = enc_left
        self.last_enc_right = enc_right

        dist_left = left_ticks / self.TICKS_PER_METER
        dist_right = right_ticks / self.TICKS_PER_METER
        dist = (dist_right + dist_left) / 2.0

        current_time = rospy.Time.now()
        d_time = (current_time - self.last_enc_time).to_sec()
        freq = 1/d_time
        if freq < 10:
            print("chock", freq)

        self.last_enc_time = current_time
       
       

        # TODO find better what to determine going straight, this means slight deviation is accounted
        if left_ticks == right_ticks:
            d_theta = 0.0
            self.cur_x += dist * cos(self.cur_theta)
            self.cur_y += dist * sin(self.cur_theta)
        else:
            d_theta = (dist_right - dist_left) / self.BASE_WIDTH
            r = dist / d_theta
            self.cur_x += r * (sin(d_theta + self.cur_theta) - sin(self.cur_theta))
            self.cur_y -= r * (cos(d_theta + self.cur_theta) - cos(self.cur_theta))

            angle = self.cur_theta + d_theta

            while angle > pi:
                angle -= 2.0 * pi
            while angle < -pi:
                angle += 2.0 * pi
            self.cur_theta = angle
        
            

        

        if abs(d_time) < 0.000001:
            vel_x = 0.0
            vel_theta = 0.0
        else:
            vel_x = dist / d_time
            vel_theta = d_theta / d_time

        return vel_x, vel_theta

    def update_publish(self, enc_left, enc_right):
        if self.start_up == 1:
            self.last_enc_right = enc_right
            self.last_enc_left = enc_left
            self.start_up = 0
        vel_x, vel_theta = self.update(enc_left, enc_right)
        self.publish_odom(self.cur_x, self.cur_y, self.cur_theta, vel_x, vel_theta)
        

    def publish_odom(self, cur_x, cur_y, cur_theta, vx, vth):
        
        quat = tf.transformations.quaternion_from_euler(0, 0, cur_theta)
        current_time = rospy.Time.now()

        br = tf.TransformBroadcaster()
        br.sendTransform((cur_x, cur_y, 0),
                         tf.transformations.quaternion_from_euler(0, 0, cur_theta),
                         current_time,
                         "base_link",
                         "odom")

        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = 'odom'

        odom.pose.pose.position.x = cur_x
        odom.pose.pose.position.y = cur_y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = Quaternion(*quat)

        odom.pose.covariance[0] = 0.02
        odom.pose.covariance[7] = 0.02
        odom.pose.covariance[14] = 99999
        odom.pose.covariance[21] = 99999
        odom.pose.covariance[28] = 99999
        odom.pose.covariance[35] = 0.05

        odom.child_frame_id = 'base_link'
        odom.twist.twist.linear.x = vx
        odom.twist.twist.linear.y = 0
        odom.twist.twist.angular.z = vth
        odom.twist.covariance = odom.pose.covariance
      
        self.odom_pub.publish(odom)
        

    
        
        

    def cb_speedCallBack(self, data):
        
        self.left_speed = data.data[0]
        self.right_speed = data.data[1]

    def stop(self):
        
        self.rc.SpeedAccelM1M2(self.address,0,0,0)    
        
    def run(self):





        rospy.init_node('roboclaw_interface_node', anonymous=True)

        port = rospy.get_param('~roboclaw_port', '/dev/ttyACM0')
        odom_freq = rospy.get_param('~odom_frequency', 100)
        p = rospy.get_param('~velocity_p', 4000)
        i = rospy.get_param('~velocity_i', 500)
        d = rospy.get_param('~velocity_d', 0.0)
        qpps = rospy.get_param('~qpps', 9000)
        motor1_max_current = rospy.get_param('~motor1_max_current', 2000)
        motor2_max_current = rospy.get_param('~motor2_max_current', 2000)
        wheel_accel = rospy.get_param('~wheel_accel', 8000)

       

        # status publisher
        #battery_status_pub = rospy.Publisher('batteryVoltage', Float32, queue_size=5)
        #battery_status_data = Float32()

        # encoder publishers
        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
        encoder_pub = rospy.Publisher('encoder', Int64MultiArray, queue_size=5)
        encoder_data = Int64MultiArray()
        
        rospy.Subscriber('wheelspeed', Int64MultiArray, self.cb_speedCallBack)

        self.address = 0x80
        self.rc = Roboclaw(port, 115200)
        self.rc.Open()

        version = self.rc.ReadVersion(self.address)
        if version[0]==False:
            print ("GETVERSION Failed")
            return
        else:
            print (repr(version[1]))
        self.rc.ResetEncoders(self.address)
        
        self.rc.SetM1VelocityPID(self.address,p,i,d,qpps)
        self.rc.SetM2VelocityPID(self.address,p,i,d,qpps)
        self.rc.SetM1MaxCurrent(self.address, motor1_max_current)
        self.rc.SetM2MaxCurrent(self.address, motor2_max_current)
        count = 0

        rate = rospy.Rate(odom_freq) # 10hz  
        self.last_enc_time = rospy.Time.now()
        self.rc.SpeedAccelM1M2(self.address,0,0,0)

        self.TICKS_PER_METER = rospy.get_param('~ticks_per_meter', 8130.0)
        self.BASE_WIDTH = rospy.get_param('~base_width', 0.25868)



        while not rospy.is_shutdown():

            

            
            self.rc.SpeedAccelM1M2(self.address, wheel_accel ,self.right_speed, self.left_speed)
            #self.rc.SpeedM1M2(self.address,self.right_speed, self.left_speed)
             

            # read encoder data
            status1, enc1, crc1 = None, None, None
            status2, enc2, crc2 = None, None, None

            try:
                status1, enc1, crc1 = self.rc.ReadEncM1(self.address)
            except ValueError:
                pass
            except OSError as e:
                rospy.logwarn("ReadEncM1 OSError: %d", e.errno)
                rospy.logdebug(e)

            try:
                status2, enc2, crc2 = self.rc.ReadEncM2(self.address)
            except ValueError:
                pass
            except OSError as e:
                rospy.logwarn("ReadEncM2 OSError: %d", e.errno)
                rospy.logdebug(e)
        
            if enc1 != None and enc2 != None:
                encoder_data.data = [enc1, enc2]
                encoder_pub.publish(encoder_data)
         
            self.update_publish(enc1, enc2)



            # read status data
            #try:
                #mainBatt =  float(self.rc.ReadMainBatteryVoltage(self.address)[1] / 10)
                #temp1 = float(self.rc.ReadTemp(self.address)[1] / 10)
                #battery_status_data.data = mainBatt
                #battery_status_pub.publish(battery_status_data)
            #except Exception as e:
                #print("Stats Error: " + str(e))

            rate.sleep()

        self.rc.SpeedAccelM1M2(self.address,0,0,0)    

if __name__ == '__main__':
    
    hw_interface = RoboClawInterface()

    try:
        
        hw_interface.run()

    except rospy.ROSInterruptException:
        pass
    
    hw_interface.stop()
    
