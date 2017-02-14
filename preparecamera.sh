# makes sure camera is on /dev/video0 and that it is not busy
ssh admin@roborio-1123-frc.local "mv /dev/video* /dev/video0 &> /dev/null; kill \$(fuser /dev/video0) &> /dev/null"
