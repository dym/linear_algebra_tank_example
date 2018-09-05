#!/bin/sh
ffmpeg -i results/scene_%09d.png -vf fps=25 -pix_fmt yuv420p out.mp4
