# pegasus-mini

roslaunch pegasus_base pegasus_base.launch

requires rosboard cloned in src of workspace - https://github.com/dheera/rosboard

Jetson Nano Notes:

- Disable nvgetty on /dev/ttyTHS1

systemctl stop nvgetty
systemctl disable nvgetty