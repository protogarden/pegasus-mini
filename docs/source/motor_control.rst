######################
Controlling the Motors
######################

The following documentation explains how to individually control the Pegasus-Mini's motors. Ensure that you have gone through the steps in :doc:`getting_started_python` first. 

.. note::
    This documentation assumes that you have been through the :doc:`python_tutorials` in order to gain an understanding of how the roboclaw.py script when importing the roboclaw module.

1. Firstly ensure your motor controller is connected to your computer via USB. 

2. Run the following lines of code in Python in order to initialize connection with motor controller. This both points to the desired ports, opens the port and then declares the address. 

.. code-block:: Python 

    import time
    from roboclaw import Roboclaw
    #Windows comport name, replace COM9 with the COM Port used by the controller.
    #rc = Roboclaw("COM9",115200)
    #If using Linux, use the following and replace /dev/ttyACM0 with the COM Port used by the controller.
    rc = Roboclaw("/dev/ttyACM0",115200)
    rc.Open()
    address = 0x80
    version = rc.ReadVersion(address)


3. There are various types of motion commands that can be send to each motor (M1 and M2), these are as follows: 

    3.1. Speed Command: The motors will try and get to the speed command (ticks/s) as fast as possible. Note that a postive value corresponds to a forward direction and a negative the opposite.

    .. code-block:: python

        rc.SpeedM1(address, target_speed)
        rc.SpeedM2(address, target_speed)

    3.2. Acceleration-Speed Command: The motors will accelerate/decelerate (ticks/s^2) to a target speed command (ticks/s). Note that acceletion value is of absoulte nature. 

    .. code-block:: python 

	    rc.SpeedAccelM1(address, acceleration, target_speed)
	    rc.SpeedAccelM2(address, acceleration, target_speed)


