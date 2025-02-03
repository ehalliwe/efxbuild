#!/bin/bash
CLIENT_IP="192.168.68.112"  # Change this to your personal machine's IP
PORT="5000"

libcamera-vid -t 0 --inline -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=$CLIENT_IP port=$PORT≈
