######################
Retrieve Encoder Data
######################

The Pegasus-Mini uses the BasicMicro Roboclaw 2x7A Motor Controller in order to control each of its drive motors, each having independant encoders. The motor controller uses these encoders inroder and provides roational information 
such as motor ticks, aswell as motor speed, in the form of ticks per a second. A tick can be desribed as a change in anglular position of the motor. The Pegasus-Mini has 64 ticks per a rotation of its drive motors. The following desribes how to obtain this
data from the motor controller using Python.

1) Firstly ensure your motor controller is connected to your computer via USB. 

2) Run the following lines of code in Python in order to initialize connection with motor controller. This both points to the desired ports, opens the port and then declares the address. 

.. code-block:: Python 

    import time
    from roboclaw import Roboclaw
    #Windows comport name
    rc = Roboclaw("COM9",115200)
    #Linux comport name
    #rc = Roboclaw("/dev/ttyACM0",115200)
    rc.Open()
    address = 0x80
    version = rc.ReadVersion(address)

3) Encoder data can be obtained for either of the motors, M1 or M2. Speed and encoder data are arrays with the following format: 

.. code-block:: Python

    [status1, encoder1_value , crc1] = rc.ReadEncM1(address)
    [status2, encoder2_value , crc1] = rc.ReadEncM2(address)
    [status1, speed1] = ReadSpeedM1(address)
    [status2, speed2] = ReadSpeedM2(address)

In order to obtain encoder data and print said data run the following line. 

.. code-block:: Python

    enc1 = rc.ReadEncM1(address)
    enc2 = rc.ReadEncM2(address)
    speed1 = rc.ReadSpeedM1(address)
    speed2 = rc.ReadSpeedM2(address)
    print("Encoder1:")
    print enc1[1]
    print "Encoder2:"
    print enc2[1]
    print format(enc2[2],'02x')
    print "Speed1:"
    print speed1[1]
    print("Speed2:")
    print speed2[1]

            