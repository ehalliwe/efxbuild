#!/bin/bash
PORT="5000"

gst-launch-1.0 -v udpsrc port=$PORT caps="application/x-rtp, encoding-name=H264, payload=96" ! \
rtph264depay ! decodebin ! videoconvert ! autovideosink sync=false
