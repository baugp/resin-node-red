#!/bin/bash

# Set timezone
if [ -n "$TIMEZONE" ]; then
  cp /usr/share/zoneinfo/$TIMEZONE /etc/localtime
  echo $TIMEZONE > /etc/timezone
fi

# Start sshd if we don't use the init system
if [ "$INITSYSTEM" != "on" ]; then
  /usr/sbin/sshd -p 22 &
fi

# OLED daemon
python /usr/src/app/PiOLED/home-stats.py &

export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

# Make the default flows available in the user library
mkdir -p /data/node-red/user/lib/flows || true
cp /usr/src/app/flows/* /data/node-red/user/lib/flows/

# Start app
node-red --settings /usr/src/app/settings.js
