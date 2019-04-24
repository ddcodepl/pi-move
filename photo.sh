#!/bin/bash
sudo /etc/init.d/webcamd stop
DATE=$(date +"%s")
fswebcam -r 1920x1080 --no-banner snap.jpg
fswebcam -r 1920x1080 --no-banner $DATE.jpg
sudo /etc/init.d/webcamd start