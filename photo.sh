#!/bin/bash
DATE=$(date +"%s")
fswebcam -r 1920x1080 --no-banner snap.jpg
cd photos && fswebcam -r 1920x1080 --no-banner $DATE.jpg