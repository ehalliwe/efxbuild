#!/bin/bash
CLIENT_IP="192.168.68.112"  # Change to your personal machine's IP
PORT="5000"

gst-launch-1.0 -v videotestsrc pattern=ball ! video/x-raw,width=160,height=120,framerate=5/1 ! \
videoconvert ! x264enc tune=zerolatency bitrate=10 speed-preset=ultrafast ! \
rtph264pay config-interval=1 pt=96 ! udpsink host=$CLIENT_IP port=$PORT
