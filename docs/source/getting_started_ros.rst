########################
Getting Started with ROS
########################

.. _software_setup:


ROS Software Setup
++++++++++++++++++

.. note::
    The following installation is assumed to be taking place on a Nvidia Jetson Nano.

Install ROS Melodic:

1.	Setup computer to accept software for package.ros.org:

.. code-block:: bash

    sudo apt-get update #download package information from all configured sources.
    sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

2. Set up your keys:

.. code-block:: bash

    sudo apt install curl # if you haven't already installed curl
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

3. Update Debian package index:

.. code-block:: bash

    sudo apt update

4. Install ROS package:

.. code-block:: bash

    sudo apt install ros-melodic-desktop-full

5. Setup the environment:

.. code-block:: bash

    echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
    source ~/.bashrc

6. Install Dependencies for building packages:

.. code-block:: bash

    sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential

7. Initialize rosdep:

.. code-block:: bash

    sudo apt install python-rosdep
    sudo rosdep init
    rosdep update

8. Install Catkin (ROS Build System):

.. code-block:: bash

    sudo apt-get install ros-melodic-catkin python-catkin-tools

9. Creating Catkin Workspace:

9.1. Make directory for workspace:

.. code-block:: bash

    mkdir -p ~/ws_(workspacename)/src
    cd ~/ws_(workspacename)/src

9.2. Install pegasus-mini package and various other dependent packages:

.. code-block:: bash

    git clone https://github.com/AprilRobotics/apriltag.git      
    git clone https://github.com/protogarden/pegasus-mini.git
    sudo apt install ros-melodic-rplidar-ros
    sudo apt-get install ros-melodic-joy ros-melodic-joystick-drivers
    sudo apt install ros-melodic-teleop-twist-joy
    sudo apt install python3-pip
    sudo pip3 install tornado
    sudo apt-get install ros-melodic-navigation
    sudo pip3 install psutil
    sudo pip install smbus
    sudo apt-get install build-essential python-dev git
    sudo pip3 install simplejpeg
    sudo pip3 install rospkg
    git clone https://github.com/dheera/rosboard.git
    sudo apt-get install ros-melodic-cartographer ros-melodic-cartographer-ros ros-melodic-cartographer-ros-msgs ros-melodic-cartographer-rviz
    rosdep install -y --from-paths . --ignore-src --rosdistro melodic

9.3. Redirect OpenCV directory for build:

.. code-block:: bash

    sudo ln -s /usr/include/opencv4/opencv2/ /usr/include/opencv
    
9.4. Build Catkin Workspace:

.. code-block:: bash

    cd ~/ws_(workspacename)
    rosdep install --from-paths src --ignore-src -r -y
    catkin config --extend /opt/ros/${ROS_DISTRO} --cmake-args -DCMAKE_BUILD_TYPE=Release
    catkin build

9.5. Source Workspace:

.. code-block:: bash

    echo "source ~/ws_(workspacename)/devel/setup.bash" >> ~/.bashrc
    source ~/.bashrc

10. Add permissions to USB ports:

.. code-block:: bash

    sudo adduser 'user' dialout

Setting Up Remote ROS Client 
+++++++++++++++++++++++++++++

In order to use ROS visual tools such as RVIZ and RQT while your Pegasus-Mini is doing what it does best, being mobile, you will need to setup a remote ROS client. You will need to install Ubuntu on this remote PC and follow the same steps to install ROS as you did for your Pegasus-Mini in :ref:`software_setup`. 

.. note::
    You need to find the IP ADDRESSES of on both your Pegasus-Mini and your remote PC. Do this by running the command [ifconfig] in terminal.


You will need to run the following commands on both your Pegasus-Mini and your remote PC respectively. Note that you will have to run these command each time you open a terminal unless you add these commands to the .bashrc file. This will run them every time you open a terminal. 

    .. list-table:: 
        :widths: 20 50 50
        :header-rows: 1
        :align: center

        * - Description
          - Pegasus-Mini
          - Remote PC 
        * - ROS_MASTER_URI
          - export ROS_MASTER_URI = http://Pegasus-Mini_IP:11311
          - export ROS_MASTER_URI = http://Pegasus-Mini_IP:11311
        * -  ROS_IP
          - export ROS_IP = Pegasus-Mini_IP
          - export ROS_IP = Remote_PC_IP 

.. note::
    Note that you will have to run these command each time you open a terminal unless you add these commands to the .bashrc file. This will run them every time you open a terminal. Do this by running source ~/.bashrc after you have run the above commands. 

            
