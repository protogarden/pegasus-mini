#!/usr/bin/env python

from argparse import ArgumentParser
import os
import cv2

import depthai
import time

import rospy 
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from numpy import asarray





pipeline = depthai.Pipeline()

# First, we want the Color camera as the output
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(500, 500)  # 300x300 will be the preview frame size, available as 'preview' output of the node
cam_rgb.setInterleaved(False)
xout_rgb = pipeline.createXLinkOut()
# For the rgb camera output, we want the XLink stream to be named "rgb"
xout_rgb.setStreamName("rgb")
# Linking camera preview to XLink input, so that the frames will be sent to host
cam_rgb.preview.link(xout_rgb.input)
bridge = CvBridge()
################################################################################

def apriltag_video(input_streams=[0], # For default cam use -> [0]
                   output_stream=False,
                   display_stream=True,
                   detection_window_name='AprilTag',
                  ):

    '''
    Detect AprilTags from video stream.

    Args:   input_streams [list(int/str)]: Camera index or movie name to run detection algorithm on
            output_stream [bool]: Boolean flag to save/not stream annotated with detections
            display_stream [bool]: Boolean flag to display/not stream annotated with detections
            detection_window_name [str]: Title of displayed (output) tag detection window
    '''



    '''
    Set up a reasonable search path for the apriltag DLL.cd 
    Either install the DLL in the appropriate system-wide
    location, or specify your own search paths as needed.
    '''

    
    img_pub = rospy.Publisher('/camera_pub/image_rect', Image, queue_size = 10)
    cam_pub = rospy.Publisher('/camera_pub/camera_info', CameraInfo, queue_size = 10)
    rospy.init_node('camera_pub')
    br = CvBridge
    fx = 3156.71852
    fy = 3129.52243
    cx = 359.097908
    cy = 239.736909
  
    cam_info = CameraInfo()
  
    

    camera_matrix = [fx, 0, cx, 0, fy, cy, 0, 0, 1]
    cam_info.K = camera_matrix
    
    with depthai.Device(pipeline) as device:

   

    # From this point, the Device will be in "running" mode and will start sending data via XLink

    # To consume the device results, we get two output queues from the device, with stream names we assigned earlier
        q_rgb = device.getOutputQueue("rgb")
    #q_nn = device.getOutputQueue("nn")

    # Here, some of the default values are defined. Frame will be an image from "rgb" stream, detections will contain nn results
        frame = None
        rate = rospy.Rate(10)

        
    #detections = []

    # Since the detections returned by nn have values from <0..1> range, they need to be multiplied by frame width/height to
    # receive the actual position of the bounding box on the image



        # Main host-side application loop
        while not rospy.is_shutdown():
            # we try to fetch the data from nn/rgb queues. tryGet will return either the data packet or None if there isn't any
            in_rgb = q_rgb.tryGet()
        

            if in_rgb is not None:
                # If the packet from RGB camera is present, we're retrieving the frame in OpenCV format using getCvFrame
                frame = in_rgb.getCvFrame()
                

    

            if frame is not None:

                img = frame
                img_msg = Image()
                stamp = rospy.Time.now()
                img_msg.height = img.shape[0]
                img_msg.width = img.shape[1]
                img_msg.step = img.strides[0]
                img_msg.encoding = 'bgr8'
                img_msg.header.frame_id = 'image_rect'
                img_msg.header.stamp = stamp
                img_msg.data = img.flatten().tolist()
                
                img_pub.publish(img_msg)

               
                cam_info.header.stamp = stamp

        #publish the camera info messages first
                cam_pub.publish(cam_info)
                rate.sleep()
        
          
               
               
            


               


                

################################################################################

if __name__ == '__main__':
    apriltag_video()