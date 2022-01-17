#############################
Dependency Installation Guide
#############################

.. note::
    The following installation is assumed to be taking place on a Nvidia Jetson Nano.

Install ROS Melodic:

1.	Setup computer to accept software for package.ros.org:

.. code-block:: bash

    sudo apt-get update download package information from all configured sources.
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

.. code-block::

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

        git clone https://github.com/protogarden/pegasus-mini.git
        sudo apt install ros-melodic-rplidar-ros
        sudo apt-get install ros-melodic-joy ros-melodic-joystick-drivers
        sudo apt install ros-melodic-teleop-twist-joy
        sudo apt install python3-pip
        sudo pip3 install tornado
        sudo pip3 install psutil
        sudo pip3 install simplejpeg
        sudo pip3 install rospkg
        git clone https://github.com/dheera/rosboard.git
        sudo apt-get install ros-melodic-cartographer ros-melodic-cartographer-ros ros-melodic-cartographer-ros-msgs ros-melodic-cartographer-rviz
        rosdep install -y --from-paths . --ignore-src --rosdistro melodic

    9.3. Build Catkin Workspace:

    .. code-block:: bash

        cd ~/ws_(workspacename)
        catkin config --extend /opt/ros/${ROS_DISTRO} --cmake-args -DCMAKE_BUILD_TYPE=Release
        catkin build

    9.4. Source Workspace:

    .. code-block:: bash

        echo "source ~/ws_(workspacename)/devel/setup.bash" >> ~/.bashrc
        source ~/.bashrc

10. Add permissions to USB ports:

.. code-block:: bash

    sudo adduser 'user' dialout
