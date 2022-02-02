##############
Remote Control
##############

The following desribes how to control the Pegasus Mini by using the ROS teleop_twist_keyboard package. See http://wiki.ros.org/teleop_twist_keyboard for full documentation. 
Ensure that all steps in the :doc:`getting_started_ros` have been completed. 

This package takes keyboard inputs and publishs command velocity to the /cmd_vel ROS topic. The pegasus_base node subsribes to these command velocitys and publishes left and right wheel speed commands to the wheelspeed topic.
Finally the rc_node node subscribes to these wheel speed commands to sends them to the motor controller. 

1.	Ensure that the ROS teleop_twist_keyboard package is installed. To do this, run the following command.

.. code-block:: bash

    sudo apt-get install ros-melodic-teleop-twist-keyboard

2. Run the Pegasus Base package by running the following command. Before performing 

.. code-block:: bash

    roslaunch pegasus_base pegasus_base.launch

2. Launch the ROS teleop_twist_keyboard package in a seperate terminal.

.. code-block:: bash

    rosrun teleop_twist_keyboard teleop_twist_keyboard.py

3. Follow the following on-screen commands to control the Pegasus-Mini. 

.. code-block:: bash


    Reading from the keyboard  and Publishing to Twist!
    ---------------------------
    Moving around:
    u    i    o
    j    k    l
    m    ,    .

    q/z : increase/decrease max speeds by 10%
    w/x : increase/decrease only linear speed by 10%
    e/c : increase/decrease only angular speed by 10%
    anything else : stop

    CTRL-C to quit