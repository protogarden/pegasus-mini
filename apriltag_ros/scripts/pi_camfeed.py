#!/usr/bin/env python3

import rospy
import yaml
import cv2
import os
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )







rospy.init_node('camera_pub')

#cam_port = rospy.get_param("/port")
#camera_type = rospy.get_param("/cam_type")

cam_standard_info = CameraInfo()
cam_standard_info.K = [1349.9794444263002, 0.0, 480.48041994199133, 0.0, 1360.4815456658516, 210.60033921891642, 0.0, 0.0, 1.0]
cam_standard_info.D = [0.19156312530171377, 0.23286435270547165, -0.038729409593406025, -0.007362024572838043, 0.0]
cam_standard_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
cam_standard_info.P = [1406.226806640625, 0.0, 477.01202548989386, 0.0, 0.0, 1401.7950439453125, 200.36270295957365, 0.0, 0.0, 0.0, 1.0, 0.0]







def pub_camera():
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    img_pub = rospy.Publisher('/camera_pub/image_rect', Image, queue_size = 10)
    cam_pub = rospy.Publisher('/camera_pub/camera_info', CameraInfo, queue_size = 10)
    rospy.init_node('camera_pub')
    bridge = CvBridge()
    rate = rospy.Rate(50)
    

    if video_capture.isOpened():

        while not rospy.is_shutdown():
            ret_val, frame = video_capture.read()
            
  
            stamp = rospy.Time.now()
            img_msg = bridge.cv2_to_imgmsg(frame, "bgr8")
            
            img_pub.publish(img_msg)

            cam_standard_info.header.stamp = stamp
            

            #publish the camera info messages first
            cam_pub.publish(cam_standard_info)
            #cv2.imshow('frame', frame)
            rate.sleep()
        

            if cv2.waitKey(1) == ord('q'):
                break

    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    pub_camera()



