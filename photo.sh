#!/bin/bash
DATE=$(date +"%s")
fswebcam -r 1920x1080 --no-banner snap.jpg
fswebcam -r 1920x1080 --no-banner $DATE.jpg