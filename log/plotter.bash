#!/usr/bin/env bash

cd /opt/maxcube-pumpe/log/

TODAY=$(date '+%Y-%m-%d')
REMOTE_LOCATION=miza:dump

python3 -c "from logger import plot_and_reset; plot_and_reset()"

scp valves.pdf "$REMOTE_LOCATION/maxcube-valves_$TODAY.pdf"
