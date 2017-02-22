[![Build Status](https://travis-ci.org/FRC-1123/frc2017-1123.svg?branch=master)](https://travis-ci.org/FRC-1123/frc2017-1123)

FRC 2017 - Team 1123
====================

This is AIM Robotics' (Team 1123) code for the 2017 FIRST Robotics Competition (FRC). The robot code is written in
Python using [RobotPy](https://robotpy.github.io/). The dashboard is written with Electron and is based on the
[FRC Dashboard](https://frcdashboard.github.io/) project.


Requirements
------------
* Python 3.x
* OpenCV 3.x
* Node.js and npm
* nodejs-legacy (only for Debian/Ubuntu)


Local Installation
------------------
After satisfying the requirements above, run the `localinstall.sh` Bash script in the `useful_scripts/` directory (make sure your computer has 
internet access). It will install the dashboard and everything needed to deploy the robot code.


Robot Installation
------------------
From a computer with pyfrc installed (e.g. one that you have run `localinstall.sh` on), run the `robotinstall.sh`
script in the `useful_scripts/` directory. Make sure the computer has internet access and that it is connected to
the robot through ethernet or USB.


Usage
-----
To start the dashboard, run `startdashboard.sh` in the `useful_scripts/` directory.
To deploy the robot code, run `python robot.py deploy` in the `robot/` directory.
If you encounter camera errors, run `preparecamera.sh` in the `useful_scripts/` directory. You may have to restart the robot code afterwards.


----------
Questions? Email me at [czhao39@gmail.com](mailto:czhao39@gmail.com).
