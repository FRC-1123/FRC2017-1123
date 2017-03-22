#!/usr/bin/env bash
# Starts the dashboard and cleans up on exit.

cd "$(dirname "$(readlink -f $0)")/../dashboard/"

# DURING COMPETITION, UNCOMMENT THE LINE BELOW AND COMMENT THE LINE BELOW IT.
# ALSO, MAKE SURE THE DRIVER STATION'S STATIC IP IS SET TO 10.11.23.6
pynetworktables2js --robot=10.11.23.2 &
# pynetworktables2js --robot=roborio-1123-frc.local &

PID=$!

# kill pynetworktables2js on EXIT
trap cleanup EXIT
function cleanup() {
    kill $PID &> /dev/null
}

npm start
