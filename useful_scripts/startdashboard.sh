#!/usr/bin/env bash
# Starts the dashboard and cleans up on exit.

cd "$(dirname "$(readlink -f $0)")/../dashboard/"
pynetworktables2js --robot=roborio-1123-frc.local &
PID=$!

# kill pynetworktables2js on EXIT
trap cleanup EXIT
function cleanup() {
    kill $PID &> /dev/null
}

npm start
