# Installs/updates RobotPy and all requirements on the robot.
# Run this locally after you have run localinstall.sh.
# Make sure you have internet access and that you are connected to the robot through ethernet or USB.
# You may have to alter version numbers (see https://www.tortall.net/~robotpy/feeds/).

robotpy-installer download-robotpy
robotpy-installer download-opkg python36-robotpy-ctre python36-numpy opencv3 python36-opencv3 python36-robotpy-cscore mjpg-streamer

robotpy-installer install-robotpy
robotpy-installer install-opkg python36-robotpy-ctre python36-numpy opencv3 python36-opencv3 python36-robotpy-cscore mjpg-streamer
