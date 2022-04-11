.. _apriltag_ros: http://wiki.ros.org/apriltag_ros. 


#############################
Pegasus-Mini Apriltag Feature
#############################

One of the Pegasus-Mini's many features its ability to use of the `apriltag_ros`_ package. This feature is an extremely powerful tool that allows you to not just continuously detect April Tags within a video stream, but to obtain the position and orientation of the april tag relative to any frame of your robot. 


.. image:: /images/apriltag/april_family.png
    :align: center
    :width: 400

AprilTag is a visual fiducial system, useful for a wide variety of tasks including augmented reality, robotics, and camera calibration. There are various April Tag family's. These can be seen in the following image:Each April tag family has a series of tags with there own unique identity's.

.. note::
    Each April tag family has a series of tags with there own unique identity's. The Pegasus-Mini Apriltag package has the ability to use tagStandard52h13, tagStandard41h12, tag36h11, tag25h9, tag16h5, tagCustom48h12, tagCircle21h7 and tagCircle49h12 family's. 

Getting Started
+++++++++++++++

The package works by subscribing to an image topic that includes camera information, and publishing an image topic showing detected tags, as well as the TF of the tags relative to your camera frame. 

1.1. In terminal, navigate to the camera publishing node. 