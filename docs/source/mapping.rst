#####################
Pegasus-Mini Mapping
#####################

The mapping feature on the Pegasus-Mini allows the robot to drive around in an enviroment and create a 2D Map of the enviroment. It does this by utilizing the Google Cartographer package. 
This package makes uses of various robot positioning data such as Lidar, Odometry and IMU * aswell as real-time simultaneous localization and mapping (SLAM). In order to perform mapping ensure that 
the lidar scanner is connected to the Pegasus-Mini and you have been through :doc:`getting_started_ros` and installed all required dependancies.

1.	Run the Pegasus-Mini mapping launch file by running the following command: 

.. code-block:: bash

    roslaunch pegasus_base pegasus_base_mapping.launch 

2.  Find the Network IP of your Pegasus-Mini. Open a web browser and type in IP-ADDRESS:8888 in order to view ROSboard. This will display all your ROS-Topics currently running, including mapping. 

.. image:: /images/mapping_guide/rosboard.PNG
    :align: center

|

3.  Move the Pegasus-Mini around slowing as described in :doc:`remote_control` by running the following command in a new terminal, in order to map your enviroment. 

.. code-block:: bash

    rosrun teleop_twist_keyboard teleop_twist_keyboard.py