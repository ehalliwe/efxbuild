#!/bin/bash
PORT="5000"

gst-launch-1.0 -v udpsrc port=$PORT caps="application/x-rtp, media=video, encoding-name=H264" ! rtph264depay ! avdec_h264 ! autovideosink sync=false