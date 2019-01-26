#!/bin/bash

cd /opt/maxcube-pumpe/log/


ADDRESS=\'192.168.0.2\'
PORT=62910
python3 -c "from logger import Logger; Logger($ADDRESS, $PORT).log()"

