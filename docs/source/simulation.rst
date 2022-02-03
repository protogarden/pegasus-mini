##############################
Pegasus-Mini Simulation
##############################

ROS Gazebo is a simulation tool that puts your Pegasus-Mini in a simulated enviroment in order to test to various things such as algorithms and other software design features. 
Ensure that you have been through :doc:`getting_started_ros` and installed all required dependancies.

1.	Run the Pegasus-Mini Gazebo launch file by running the following command: 

.. code-block:: bash

    roslaunch pegasus_simulation pegasus_gazebo.launch

The Gazebo tool will launch and spawn your Pegasus-Mini into the simulation with a simulated Lidar Scanner. 

.. image:: /images/simulation_guide/simulation_guide.png
    :align: center

|

2.  In order to move the Pegasus-Mini around within the world you can use the ROS teleop_twist_keyboard package as described here :doc:`remote_control` by opening
a seperate terminal and running the following command:

.. code-block:: bash

    rosrun teleop_twist_keyboard teleop_twist_keyboard.py
