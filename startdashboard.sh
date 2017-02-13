cd dashboard/
pynetworktables2js --robot=roborio-1123-frc.local &
PID=$!

# kill pynetworktables2js on EXIT
trap cleanup EXIT
function cleanup() {
    kill $PID &> /dev/null
}

npm start
