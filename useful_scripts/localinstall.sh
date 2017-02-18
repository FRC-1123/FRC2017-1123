#!/usr/bin/env bash
# Installs the dashboard and everything needed to deploy the robot code.
# Make sure you have installed Python 3 and Node.js before running this.
# If you wish to use OpenCV, you will have to install it yourself (make sure to get OpenCV 3).

pip install -r $(dirname $(readlink -f $0))/../requirements.txt
cd $(dirname $(readlink -f $0))/../dashboard/
npm install
