#!/bin/bash

#cd /opt/maxcube-pumpe/log/

TODAY=$(date '+%Y-%m-%d')
REMOTE_LOCATION=miza:dump/maxcube

python3 -c "from plotter import plot; plot('{TODAY}')"

scp valves.pdf "$REMOTE_LOCATION/maxcube-valves_$TODAY.pdf"
scp temps.pdf  "$REMOTE_LOCATION/maxcube-temps_$TODAY.pdf"

scp ${TODAY}-log.csv  "$REMOTE_LOCATION/logs/"