#!/bin/sh
time /usr/local/bin/ffmpeg -i results/scene_%09d.png -vf fps=25 out.mp4
