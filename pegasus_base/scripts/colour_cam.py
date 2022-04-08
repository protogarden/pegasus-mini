#!/usr/bin/env python3

import rospy
import cv2
import depthai as dai
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setVideoSize(500, 500)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

cam_info = CameraInfo()



camera_matrix = [692.197324430714, 0.0, 272.85376299724896, 0.0, 666.8629839228164, 268.4270301686383, 0.0, 0.0, 1.0]
cam_info.K = camera_matrix
cam_info.D = [0.21989472450195113, -0.9680733520754665, 0.03908595310462266, 0.006195633961802485, 0.0]
cam_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
cam_info.P = [709.3319702148438, 0.0, 275.65464230645375, 0.0, 0.0, 668.7578125, 280.5455521137919, 0.0, 0.0, 0.0, 1.0, 0.0]


# Linking
camRgb.video.link(xoutVideo.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    img_pub = rospy.Publisher('/camera_pub/image_rect', Image, queue_size = 10)
    cam_pub = rospy.Publisher('/camera_pub/camera_info', CameraInfo, queue_size = 10)
    rospy.init_node('camera_pub')

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
    rate = rospy.Rate(10)

    while True:
        videoIn = video.get()
        img = videoIn.getCvFrame()
        img_msg = Image()
        stamp = rospy.Time.now()
        img_msg.height = img.shape[0]
        img_msg.width = img.shape[1]
        img_msg.step = img.strides[0]
        img_msg.encoding = 'bgr8'
        img_msg.header.frame_id = 'camera'
        img_msg.header.stamp = stamp
        img_msg.data = img.flatten().tolist()
        
        img_pub.publish(img_msg)

        cam_info.header.stamp = stamp
        rate.sleep()

        #publish the camera info messages first
        cam_pub.publish(cam_info)
      

        # Get BGR frame from NV12 encoded video frame to show with opencv
        # Visualizing the frame on slower hosts might have overhead
        #cv2.imshow("video", videoIn.getCvFrame())

        if cv2.waitKey(1) == ord('q'):
            break