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
        self.address = 0x80
        self.rc = Roboclaw("/dev/ttyACM0", 115200)

    def cb_speedCallBack(self, data):
        self.left_speed = data.data[0]
        self.right_speed = data.data[1]

    def stop(self):
        self.rc.SpeedAccelM1M2(self.address,0,0,0)    
        
    def run(self):
        self.rc.Open()

        version = self.rc.ReadVersion(self.address)

        if version[0]==False:
            print ("GETVERSION Failed")
            return
        else:
            print (repr(version[1]))

        rospy.init_node('roboclaw_interface_node', anonymous=True)

        rate = rospy.Rate(10) # 10hz    

        # status publisher
        battery_status_pub = rospy.Publisher('batteryVoltage', Float32, queue_size=5)
        battery_status_data = Float32()

        # encoder publishers
        encoder_pub = rospy.Publisher('encoder', Int64MultiArray, queue_size=5)
        encoder_data = Int64MultiArray()
        
        rospy.Subscriber('wheelspeed', Int64MultiArray, self.cb_speedCallBack)

        while not rospy.is_shutdown():

            self.rc.SpeedM1M2(self.address,self.right_speed, self.left_speed)    

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

            # read status data
            try:
                mainBatt =  float(self.rc.ReadMainBatteryVoltage(self.address)[1] / 10)
                #temp1 = float(self.rc.ReadTemp(self.address)[1] / 10)
                battery_status_data.data = mainBatt
                battery_status_pub.publish(battery_status_data)
            except Exception as e:
                print("Stats Error: " + str(e))

            rate.sleep()

        self.rc.SpeedAccelM1M2(self.address,0,0,0)    

if __name__ == '__main__':
    hw_interface = RoboClawInterface()

    try:
        hw_interface.run()

    except rospy.ROSInterruptException:
        pass
    
    hw_interface.stop()
    
