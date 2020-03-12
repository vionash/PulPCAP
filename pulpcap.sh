#!/usr/bin/env bash

#Tracerouting to KIBP USA IP, storing as TR
TR=$(traceroute 10.255.0.1)
#Grabs tel-, and 16 digits after.
KIBPLocation=$(echo $TR | grep -o -P '.{0,0}tel-.{0,16}')
#echo $KIBPLoc

#export to enviro variable
export KIBPLocation
python pulpcap.py