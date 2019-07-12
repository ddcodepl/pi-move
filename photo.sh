#!/bin/bash
DATE=$1
cd ai_model/test && fswebcam -r 1920x1080 --no-banner snap.jpg
cd photos && fswebcam -r 1920x1080 --no-banner $DATE.jpg