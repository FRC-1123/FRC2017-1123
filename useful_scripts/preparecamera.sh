#!/usr/bin/env bash
# Makes sure all camera devices are not busy.

ssh admin@roborio-1123-frc.local "kill \$(fuser /dev/video*) &> /dev/null"
