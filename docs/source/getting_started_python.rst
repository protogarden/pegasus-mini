#############################
Getting Started with Python
#############################

The following documentation describes the basics of getting started with Python, including installing Python and creating and running a Python script.
For this documentation it is recommended that you run Python on Ubuntu. 

.. note::
    The following documentation assumes that you have Ubuntu 16.10 or newer installed, either running independantly on a PC, or on a virtual machine.

.. image:: /images/ubuntu-logo.png
    :align: center
    :width: 300


Getting Started with Python on Ubuntu 
+++++++++++++++++++++++++++++++++++++

.. note::
    If you are completely new to Ubuntu, check out https://ubuntu.com/tutorials/command-line-for-beginners#1-overview for the basics, including using Terminal and navigating to folders and files.

1.1. If you are using Ubuntu 16.10 or newer which we recommended, then run the following commands in terminal to install Python 3.6:

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install python3.6

1.2. Create your Python script by using a text editor within Ubuntu and saving it as a .py file type. Then, navigate in terminal to where you saved your file and run the following command to make your script executable: 

.. code-block:: python 

    chmod +x SCRIPTNAME.py
    
1.3. Finally, run your script using the following command: 

.. code-block:: python 
    
	Python3 SCRIPTNAME.py






