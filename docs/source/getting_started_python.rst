.. _Ubuntu Tutorials: https://www.slamtec.com/en/Lidar/A1

.. _Python Tutorials: https://docs.python.org/3/tutorial/. 



#############################
Getting Started with Python
#############################

The following documentation describes the basics of getting started with Python, including installing Python, followed by creating and then running a Python script.
For this documentation it is recommended that you run Python on Ubuntu. 

.. note::
    The following documentation assumes that you have Ubuntu 16.10 or newer installed, either running independently on a PC, or on a virtual machine. If you are completely new to Ubuntu, check out `Ubuntu Tutorials`_ for the basics, including importantly using Terminal and navigating to folders and files.

.. image:: /images/ubuntu-logo.png
    :align: center
    :width: 300

1. Installing Python 3:

    1.1. If you are using Ubuntu 16.10 or newer which we recommended, then run the following commands in terminal to install Python 3.6:

    .. code-block:: bash

        sudo apt-get update
        sudo apt-get install python3.6

2. Creating and running your python script

    2.1. Create your Python script by using a text editor within Ubuntu and saving it as a '.py' file type. Then, navigate in terminal to where you saved your file and run the following command to make your script executable: 

    .. code-block:: python 

        chmod +x SCRIPTNAME.py
    
    2.2. Finally, run your script using the following command: 

    .. code-block:: python 
    
	    Python3 SCRIPTNAME.py

3. The next step in :doc:`getting_started_python` would be make yourself familiar with the Python language itself. This includes making use of flow control tools and data structures, amoungst many other things. For a comprehensive guide and tutorials in programming in Python, check out `Python Tutorials`_.







