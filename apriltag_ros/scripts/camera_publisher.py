#!/usr/bin/env python3

import rospy
import yaml
import cv2
import os
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo






rospy.init_node('camera_pub')
cam_port = 0
camera_type = "oak_d" #if using OAK-d camera, camera_type = "oak_d". If using standard webcam camera_type = "standard".

#cam_port = rospy.get_param("/port")
#camera_type = rospy.get_param("/cam_type")

cam_standard_info = CameraInfo()
cam_standard_info.K = [712.1036081760766, 0.0, 467.68377603664027, 0.0, 712.403233695187, 269.04193985198145, 0.0, 0.0, 1.0]
cam_standard_info.D = [0.021533613848944824, -0.09687445622248622, 0.002708932663089853, -0.004650287718603307, 0.0]
cam_standard_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
cam_standard_info.P = [703.6085815429688, 0.0, 461.8930612015138, 0.0, 0.0, 714.2974853515625, 270.0070402640449, 0.0, 0.0, 0.0, 1.0, 0.0]




# Create pipeline
if camera_type == "oak_d": 
    import depthai as dai
    pipeline = dai.Pipeline()
    camRgb = pipeline.create(dai.node.ColorCamera)
    xoutVideo = pipeline.create(dai.node.XLinkOut)
    xoutVideo.setStreamName("video")
    camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setVideoSize(1920, 1080)
    xoutVideo.input.setBlocking(False)
    xoutVideo.input.setQueueSize(1)
    #camera_information:
    cam_info = CameraInfo()
    cam_info.K = [712.1036081760766, 0.0, 467.68377603664027, 0.0, 712.403233695187, 269.04193985198145, 0.0, 0.0, 1.0]
    cam_info.D = [0.021533613848944824, -0.09687445622248622, 0.002708932663089853, -0.004650287718603307, 0.0]
    cam_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    cam_info.P = [703.6085815429688, 0.0, 461.8930612015138, 0.0, 0.0, 714.2974853515625, 270.0070402640449, 0.0, 0.0, 0.0, 1.0, 0.0]
    # Linking
    camRgb.video.link(xoutVideo.input)

    with dai.Device(pipeline) as device:

        img_pub = rospy.Publisher('/camera_pub/image_rect', Image, queue_size = 10)
        cam_pub = rospy.Publisher('/camera_pub/camera_info', CameraInfo, queue_size = 10)
        

        video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        rate = rospy.Rate(5)
        rospy.loginfo("/port: %s, /cam_type: %s", cam_port, camera_type)

        while not rospy.is_shutdown():
            videoIn = video.get()
            i = videoIn.getCvFrame()
            img =cv2.resize(i,(960,540))
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


elif camera_type == "standard":
    vid = cv2.VideoCapture(cam_port)
    img_pub = rospy.Publisher('/camera_pub/image_rect', Image, queue_size = 10)
    cam_pub = rospy.Publisher('/camera_pub/camera_info', CameraInfo, queue_size = 10)
    rospy.init_node('camera_pub')
    rospy.loginfo("/port: %s, /cam_type: %s", cam_port, camera_type)

    while not rospy.is_shutdown():
        ret, frame = vid.read()
        img =cv2.resize(frame,(960,540))
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

        cam_standard_info.header.stamp = stamp
        rate.sleep()

        #publish the camera info messages first
        cam_pub.publish(cam_standard_info)
        cv2.imshow('frame', img)
    

        if cv2.waitKey(1) == ord('q'):
            break

else: 
    rospy.loginfo("No camera parameters received")



'''

Oak-D parameters with the above config: 

D = [0.021533613848944824, -0.09687445622248622, 0.002708932663089853, -0.004650287718603307, 0.0]
K = [712.1036081760766, 0.0, 467.68377603664027, 0.0, 712.403233695187, 269.04193985198145, 0.0, 0.0, 1.0]
R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
P = [703.6085815429688, 0.0, 461.8930612015138, 0.0, 0.0, 714.2974853515625, 270.0070402640449, 0.0, 0.0, 0.0, 1.0, 0.0]

'''


