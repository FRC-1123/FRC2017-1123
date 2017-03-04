#!/usr/bin/env bash
# Makes sure all camera devices are not busy.

ssh admin@10.11.23.2 "kill \$(fuser /dev/video*) &> /dev/null"
