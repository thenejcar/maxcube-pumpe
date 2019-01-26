#!/bin/bash

cd /opt/maxcube-pumpe/log/

TODAY=$(date '+%Y-%m-%d')
REMOTE_LOCATION=miza:dump/maxcube

python3 -c "from plotter import plot_and_reset; plot_and_reset()"

scp valves.pdf "$REMOTE_LOCATION/maxcube-valves_$TODAY.pdf"
