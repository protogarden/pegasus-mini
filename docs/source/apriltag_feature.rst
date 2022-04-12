.. _apriltag_ros: http://wiki.ros.org/apriltag_ros

.. _OAK-D Camera: https://store.opencv.ai/products/oak-d

.. _ROS Camera Calibration: http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration

.. _Checkered Board: http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration?action=AttachFile&do=view&target=check-108.pdf


#############################
AprilTag Package
#############################

One of the Pegasus-Mini's many features its ability to use of the `apriltag_ros`_ package. This feature is an extremely powerful tool that allows you to not just continuously detect April Tags within a video stream, but to obtain the position and orientation of the april tag relative to any frame of your robot. This is by default relative to camera frame.


.. image:: /images/apriltag/april_family.png
    :align: center
    :width: 400

AprilTag is a visual fiducial system, useful for a wide variety of tasks including augmented reality, robotics, and camera calibration. There are various April Tag family's. Each April tag family has a series of tags with there own unique identity's. The family's can be seen in the following image:

.. note::
    Each April tag family has a series of tags with there own unique identity's. The Pegasus-Mini Apriltag package has the ability to use tagStandard52h13, tagStandard41h12, tag36h11, tag25h9, tag16h5, tagCustom48h12, tagCircle21h7 and tagCircle49h12 family's. 

Getting Started
+++++++++++++++

The package works by subscribing to an image topic using the provided camera information (camera matrix), and publishing an image topic showing detected tags, as well as the TF of the tags relative to your camera frame. 

.. image:: /images/apriltag/apriltag_demo.png
    :align: center
    :width: 400

.. note::
    The Pegasus-Mini AprilTag package can either be used with any webcam or the `OAK-D Camera`_. We suggest the OAK-D Camera as it has its own onboard processor with many powerful capabilities. 

First things first, we need to configure our camera publishing node for the choice of camera. Navigate to the following directory /pegasus-mini/apriltag_ros/scripts and open up camera_publisher.py in any text editor. Edit the following parameters to suit your associated camera choice:

.. code-block:: bash

    camera_type = "oak_d" #If using OAK-d camera, camera_type = "oak_d". If using standard webcam camera_type = "standard".
    cam_port = 0 #Default it 0, when launching the publishing node if error is throw regarding your camera port change this variable to 1. 
    

If you are using the OAK-D camera you will need to install the Oak-D depth ai module, otherwise you can skip this step. This can be done by navigating to where you desire to install the module, then running the following set of commands:

.. code-block:: bash

    git clone https://github.com/luxonis/depthai-python.git
    cd depthai-python
    echo "export OPENBLAS_CORETYPE=ARMV8" >> ~/.bashrc
    cd examples
    python3 install_requirements.py
    source ~/.bashrc

You now need to tell the Pegasus-Mini Apriltag package which tag family to look for, as well as their corresponding tag ID's. This can be done in the settings.yaml and tags.yaml files found in the /apriltag_ros/config directory.

.. image:: /images/apriltag/tag_36h11.png
    :align: center
    :width: 400

Camera Calibration
+++++++++++++++++++++

.. note::
    When using the OAK-D camera there is no need to provide camera parameters though the calibration process as we have done that part for you. However, if you are using your own camera you need to calibrate it yourself. The calibration process makes use of a printed checkered board. This can be found here `Checkered Board`_.

First things first, install camera calibration dependencies:

.. code-block:: bash

    rosdep install camera_calibration

Ensure that your camera is connected to your processing unit, navigate to the following directory /pegasus-mini/apriltag_ros/scripts/, and launch your camera publishing node as follows: 

.. code-block:: bash

    python3 camera_publisher.py

Follow the `ROS Camera Calibration`_ tutorial, using the following command in a separate terminal to launch the application: 

.. code-block:: bash

    rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.025 image:=/camera_pub/image_rect camera:=/  --no-service-check

Once you have complete Camera Calibration and will need to add your camera parameters to the Pegasus-Mini camera publishing node. In the same way that your configured the node for your choice of camera, you will need to add your obtained camera parameters. These are following parameters that need to be edited in the node:

.. code-block:: bash

    cam_standard_info.K = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    cam_standard_info.D = [0.0, 0.0, 0.0, 0.0, 0.0]
    cam_standard_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    cam_standard_info.P = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]

Running Apriltag Package
+++++++++++++++++++++++++++++

Apriltag package requires your camera publishing node to be running. Navigate to /pegasus-mini/apriltag_ros/scripts/ and run the following command: 

.. code-block:: bash

    python3 camera_publisher.py
    
You can now launch the apriltag package by running the following command in a separate terminal: 

.. code-block:: bash

    roslaunch apriltag_ros apriltag.launch

.. image:: /images/apriltag/april.png
    :align: center
    :width: 700



