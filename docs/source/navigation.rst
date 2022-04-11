##################################
Getting Started with Navigation
##################################

The following documentation describes how to get your robot autonomously navigating an environment. 

.. note::
    In order to perform navigation it is required that you a RP-Lidar sensor installed and connected to your Pegasus-Mini.

First things first, your Pegasus-Mini need 2D representation of its environment. This is obtained by using the Pegasus-Mini mapping feature. 

1. Creating a Map  
++++++++++++++++++

1.1 Place your Pegasus-Mini within the environment in which you wish to map. 

.. note::
    The position from which you start the mapping process will be your initial position on the map with the co-ordinates and orientation of (x, y, theta) = 0, 0, 0. 

1.2. Launch the Pegasus-Mini mapping package by running the following command: 

.. code-block:: bash

    roslaunch pegasus_base pegasus_base_mapping.launch

1.3. Drive your robot slowly around your environment by making use of :doc:`remote_control`. 

.. image:: /images/navigation_guide/nav_map_ref.png
    :align: center
    :width: 500

1.4. You can now save the map by use of the ROS map_server. Within your terminal, navigate to following directory /pegasus_navigation/maps and run the following command to save your map: 

.. code-block:: bash

    rosrun map_server map_saver -f map_name

2. Navigating a Map
+++++++++++++++++++++

2.1. Now that you have a map to navigate, you can launch the Pegasus-Mini navigation package. Before that is done, you need to tell the navigation package which to map to load. Navigate to the following directory /pegasus-mini/pegasus_navigation/launch, open pegasus_nav.launch and change the following argument to point to the map you saved:

.. code-block:: bash

    <arg name="map_file" default="$(find pegasus_navigation)/maps/your_map_name.yaml"/>   

2.2. Launch the Pegasus-Mini Navigation package by running the following file: 

.. code-block:: bash 

    roslaunch pegasus_navigation pegasus_nav.launch

2.3. The Pegasus-Mini navigation package needs two sets of information. The first is an initial 2D Pose estimation when the package is first launched. This allows the package to get an estimation of where your robot currently is. The second set of information is a 2D Navigation goal. It is suggested that you launch RVIZ on a remote PC as described in ????, and then running the following command: 

.. code-block:: bash 

    rosrun rviz rviz

The following image shows ROS Visualization launched. Add three displays to your RVIZ. The first being your map using the /map topic, the second being the Pegasus-Mini Robot-model and finally TF. A 2D initial estimation and 2D navigation goal can be sent to the Pegasus-Mini navigation package by using these corresponding tools in RVIZ.

.. image:: /images/navigation_guide/nav1.png
    :align: center
    :width: 500








