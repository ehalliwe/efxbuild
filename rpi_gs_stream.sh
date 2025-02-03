#!/bin/bash
CLIENT_IP="192.168.68.112"  # Replace with your PC's IP
PORT="5000"

gst-launch-1.0 -v libcamerasrc ! video/x-raw,width=640,height=480,framerate=30/1 ! \
videoconvert ! x264enc tune=zerolatency bitrate=1000 speed-preset=ultrafast ! \
rtph264pay config-interval=1 pt=96 ! udpsink host=$CLIENT_IP port=$PORT